# -*- coding: utf-8 -*-

import oss2
import logging
import json
import sys
import base64
from itertools import islice

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)


def get_oss_file(param):
    endpoint = 'oss-cn-beijing.aliyuncs.com'
    bucket = 'video-match'
    auth = oss2.StsAuth(
        param.get('id'),
        param.get('secret'),
        param.get('stoken'),
    )
    bucket_obj = oss2.Bucket(auth, endpoint, bucket)
    '''
    here we just known the file path, can be change  to your self path , or just list the bucket
    '''
    bucket_obj.get_object_to_file(
        "mgtv_contest/res/image/videoTrack/research_datasets_1.zip", "./research_datasets_1.zip")
    bucket_obj.get_object_to_file(
        "mgtv_contest/res/image/videoTrack/research_datasets_2.zip", "./research_datasets_2.zip")
    bucket_obj.get_object_to_file(
        "mgtv_contest/res/image/videoTrack/sample.zip", "./sample.zip")
    bucket_obj.get_object_to_file(
        "mgtv_contest/res/image/videoTrack/test_a.zip", "./test_a.zip")
    bucket_obj.get_object_to_file(
        "mgtv_contest/res/image/videoTrack/val.zip", "./val.zip")

def main():
    if len(sys.argv) != 2:
        logging.error("please run with : python oss.py <code>")
        sys.exit(1)
    obj = json.loads(base64.b64decode(sys.argv[1]))
    get_oss_file(obj)


if __name__ == "__main__":
    main()
