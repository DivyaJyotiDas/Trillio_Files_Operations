import hashlib
import threading
import time

FILE = '/dev/vda1'
T1_DEST_FILE = '/home/afour/PycharmProjects/Trillio_Files_Operations/logs/vda_one.img'


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def chunks_md5(chunks):
    res = hashlib.md5(chunks)
    return res.hexdigest()


def size_of_file(fp):
    # returns the size of file in bytes.
    return fp.seek(0, 2)


def num_process_creation(size):
    # Logic to create num of threads.
    power = 2 ** 10
    n = 0

    while size > power:
        size /= power
        n += 1

    return pow(2, n)


def execution_time(outer):
    """
    :param outer:
    :return:
    """

    def inner(fp, start_chunk, end_chunk, dest_fp, pid):
        start_time = time.time()
        outer(fp, start_chunk, end_chunk, dest_fp, pid)
        end_time = time.time()
        print(end_time - start_time)

    return inner


def read_in_chunks(fp, start_chunk, end_chunk, small_chunk_size=2**20):
    """
        Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k.
        Smart way of generating data on fly rather keeping all data in memory
    """

    num = 1
    while end_chunk >= num * small_chunk_size:
        data = fp.read(small_chunk_size)
        checksum = chunks_md5(data)
        if not data:
            break
        num += 1
        yield {'data': data, 'checksum': checksum}

    data = fp.read(abs(end_chunk - (num - 1) * small_chunk_size))
    checksum = chunks_md5(data)
    yield {'data': data, 'checksum': checksum}


@execution_time
def read_file(fp, start_chunk, end_chunk, dest_fp, pid):
    """
    :param fp:
    :param start_chunk:
    :param end_chunk:
    :param dest_fp:
    :return:
    """
    progress, count = 0, 0
    fp.seek(start_chunk)
    dest_fp.seek(start_chunk)

    chunks = end_chunk - start_chunk
    data = read_in_chunks(fp, start_chunk, end_chunk)

    for piece in data:
        print(piece.get('checksum'))
        count += 1
        try:
            init_pointer = dest_fp.tell()
            dest_fp.write(piece.get('data'))
            end_pointer = dest_fp.tell()
            dest_fp.seek(init_pointer)
            my_data = dest_fp.read(end_pointer - init_pointer)

            checksum = chunks_md5(my_data)
            if piece.get('checksum') == checksum:
                progress += (len(piece.get('data')) / chunks) * 100
                print('{}:- {} % completed out of {} bytes.'.format(threading.current_thread().name,
                                                                    progress,
                                                                    end_chunk))

                pid.progress = progress
                pid.save(update_fields=['progress'])
        except Exception as e:
            # TODO: Write logic for retry here.
            print('Exception:- ', e)


