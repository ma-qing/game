# from django.test import TestCase
#
# # Create your tests here.
# # -*- coding: utf-8 -*-
# import zlib, glob, os, sys, struct
#
# filelist = []
#
# class FileVisitor:
#     def __init__(self, startDir=os.curdir):
#         self.startDir = startDir
#     def run(self):
#         for dirname, subdirnames, filenames in os.walk(self.startDir, True):
#             for filename in filenames:
#                 self.visit_file(os.path.join(dirname, filename))
#     def visit_file(self, pathname):
#         filelist.append({'filename':pathname, 'size':0, 'zlib_size':0, 'offset':0, 'relative_filename': pathname.replace(os.path.normpath(self.startDir)+os.sep, '')})
#         #print filelist[-1]['relative_filename']
#
#
# if __name__ == "__main__":
#     if len(sys.argv[1]) < 3:
#         print('few parameter')
#     else:
#         source_dirname = sys.argv[1]
#         out_filename = sys.argv[2]
#         FileVisitor(source_dirname).run()
#         total = len(filelist)
#         fp = open(out_filename + '~', 'wb')
#         fp.write(b'\x64\x00\x00\x00')
#         fp.write(struct.pack('I', len(filelist)))
#         fp.write(struct.pack('I', 0))
#         fp.write(struct.pack('I', 0))
#         offset = 16
#         for index in range(total):
#             item = filelist[index]
#             item['offset'] = offset
#             infile = open(item['filename'], 'rb')
#             text = infile.read()
#             infile.close()
#             item['size'] = len(text)
#             text = zlib.compress(text)
#             item['zlib_size'] = len(text)
#             fp.write(text)
#             offset += item['zlib_size']
#             print(u'已压缩文件 %d/%d' % (index+1, total))
#         filename_table_offset = offset
#         for index in range(total):
#             item = filelist[index]
#             fp.write(struct.pack('H', len(item['relative_filename'])))
#             fp.write(item['relative_filename'].encode('utf8'))
#             fp.write(b'\x01\x00\x00\x00')
#             fp.write(struct.pack('I', item['offset']))
#             fp.write(struct.pack('I', item['size']))
#             fp.write(struct.pack('I', item['zlib_size']))
#             offset += 2 + len(item['relative_filename']) + 16
#             print(u'已输出路径 %d/%d' % (index+1, total))
#         filename_table_len = offset - filename_table_offset
#         fp.close()
#
#         fp = open(out_filename + '~', 'rb')
#         fp.read(16)
#         ret = open(out_filename, 'w')
#         ret.write('\x64\x00\x00\x00')
#         ret.write(str(len(filelist)))
#         ret.write("\n")
#         ret.write(str(filename_table_offset))
#         ret.write("\n")
#
#         ret.write(str(filename_table_len))
#         ret.write("\n")
#
#         copy_bytes = 16
#         total_bytes = offset
#         # while True:
#         #     text = fp.read(2**20)
#             # ret.write(text)
#             # copy_bytes += len(text)
#             # print(u'最后的拷贝 %d%%' % (copy_bytes*100.0/total_bytes))
#             # if not text:
#             #     break
#         fp.close()
#         ret.close()
#         os.remove(out_filename + '~')
#
#
# import gzip
# import tarfile
# tar = tarfile.open("static.tar.gz", "w:gz")
# tar.add("E:\WorkCode\game\static", arcname="static")
# tar.close()
#
# url = "http://localhost:8000/api/interaction/viewGzip"
# import requests
# result = requests.post(url)
# with open("接受.tar.gz",  "wb") as f:
#     f.write(result.content)
import zipfile
import os


def zip_yasuo(start_dir, end_dir):
    file_news = end_dir + '/static.zip'
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        file_path = dir_path.replace(start_dir, '')
        file_path = file_path and file_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), file_path+filename)
    z.close()
    return file_news


if __name__ == "__main__":
    Start_dir = "E:\WorkCode\game\static"
    end_dir = "E:\WorkCode\game\yasuo\yasuo"
    zip_yasuo(Start_dir, end_dir)
