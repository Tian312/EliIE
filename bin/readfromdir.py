__author__ = 'kangtian'
import os,glob

def get_file_list(dir_path, extension_list):
    '''
fuction: get_file_list(dir_path,extension_list)
parms:
dir_path - a string of directory full path. eg. 'D:user'
extension_list - a list of file extension. eg. ['zip']
return: a list of file full path. eg. ['D:user1.zip', 'D:user2.zip']
'''
    os.chdir(dir_path)
    file_list = []
    for extension in extension_list:
        extension = '*.' + extension
        file_list += [os.path.realpath(e) for e in glob.glob(extension) ]
    return file_list

