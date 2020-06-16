import os
import hashlib
import sys

MAX_BLOCK_SIZE = 1024 * 1024

def load_snapshot_folder(PROJECT_FOLDER):
  snapshot_folder = '{0}/.snapshot'.format(PROJECT_FOLDER)
  if not os.path.exists(snapshot_folder):
    print('Snapshot does not exists')
    return -1

  return snapshot_folder

def init(PROJECT_FOLDER):
  snapshot_folder = load_snapshot_folder(PROJECT_FOLDER)
  if (snapshot_folder == -1):
    snapshot_folder = '{0}/.snapshot'.format(PROJECT_FOLDER)
    print('Initializing snapshot...')
    os.mkdir(snapshot_folder)
    print('Snapshot initialized')
  
  return snapshot_folder

def snap(PROJECT_FOLDER):
  print('Snapping...')

  snapshot_folder = load_snapshot_folder(PROJECT_FOLDER)
  if (snapshot_folder == -1):
    print('Please init snapshot')
    exit(3)

  dirs = os.listdir(PROJECT_FOLDER)
  
  if '.snapshot' not in dirs:
    print('No snapshot found. Please initialize snapshot')
    exit(4)

  dirs.remove('.snapshot')
  copy_project_to_snapshot(PROJECT_FOLDER, snapshot_folder)



def copy_project_to_snapshot(source, destination):
  dirs = os.listdir(source)

  if '.snapshot' in dirs:
    dirs.remove('.snapshot')

  for blob in dirs:
    source_blob_dir = '{0}/{1}'.format(source, blob)
    
    if os.path.isfile(source_blob_dir):
      transfer_file(source_blob_dir, destination, blob)
      continue

    destination_blob_dir = '{0}/{1}'.format(destination, blob)
    
    if not os.path.exists(destination_blob_dir):
      os.mkdir(destination_blob_dir)
    
    copy_project_to_snapshot(source_blob_dir, destination_blob_dir)



def transfer_file(source_blob_dir, destination, blob):
  destination_blob_dir = '{0}/{1}'.format(destination, blob)

  if (os.path.exists(destination_blob_dir)):
    source_file_hash = compute_file_hash(source_blob_dir)
    destination_file_hash = compute_file_hash(destination_blob_dir)

    if source_file_hash == destination_file_hash:
      print('{0} is not changed.'.format(source_blob_dir))
      return

  source_blob = open(source_blob_dir, 'rb')
  destination_blob = open(destination_blob_dir, 'w+b')

  while True:
    blob_data = source_blob.read(MAX_BLOCK_SIZE)
    if not blob_data:
      break
    destination_blob.write(blob_data)

  source_blob.close()
  destination_blob.close()


def compute_file_hash(file_src):
  source_file = open(file_src, 'rb')
  
  sha256 = hashlib.sha256()

  while True:
    source_data = source_file.read(MAX_BLOCK_SIZE)
    if not source_data:
      break

    sha256.update(source_data)

  return sha256.hexdigest()

def help():
  help = open('./help', 'r')
  print(help.read())
  help.close()

def intro():
  intro = open('./intro', 'r')
  print(intro.read())
  intro.close()

  
def main():
  args = sys.argv
  if (len(args) <= 1):
    intro()
    help()
    return

  command = args[1]
  if (command == 'init'):
    if (len(args) < 3):
      print('Please specify project folder')
      help()
      return

    PROJECT_FOLDER = args[2]
    init(PROJECT_FOLDER)
    return

  if (command == 'snap'):
    if (len(args) < 3):
      print('Please specify project folder')
      help()
      return

    PROJECT_FOLDER = args[2]      
    snap(PROJECT_FOLDER)
    return

  if (command == '-v'):
    intro()
    return

  print('Invalid command')
  intro()
  help()
  return

if __name__ == '__main__':
  main()
