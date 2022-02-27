import sys
from cloud_catcher.multi_catch import multi_catch
from batches.batches import batches
import multiprocessing
multiprocessing.freeze_support()


def main(batch_name):
    if not batch_name:
        return print('Please type in name of the batch')
    batch = batches.get(batch_name)
    if not batch:
        return print('No batch named:', batch_name)
    if __name__ == '__main__':
        try:
            multi_catch(batch)
            print('Batch {} done! :)'.format(batch_name))
        except KeyboardInterrupt:
            print('Exiting')


if __name__ == '__main__':
    main(sys.argv[1])
