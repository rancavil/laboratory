#!/usr/bin/env python
#
# Copyright 2015 Rodrigo Ancavil del Pino
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import httplib
import re
import json
import datetime

def fetch_page():
     """
      connect and fetch the main page from stackoverflow
     """
     conn = httplib.HTTPConnection('stackoverflow.com')
     conn.request('GET','/')
     site = conn.getresponse()
     if site.status == 200:
          html = site.read()
          return html.replace('\n','').replace('\r','')
     else:
          return None

def parse_html(html):
     """
      parse html code,  finding all questions with their related data from main html page
     """
     data = list()
     for match in re.finditer('<div class="question-summary narrow"\s*id="question-summary-[0-9]+"\s*>.*?</div>\s*<div class="started">',html,re.U):
          data_json = extract_data_2_json(match.group())
          if data_json != None:
               data.append(data_json)

     return data

def extract_data_2_json(match):
     """
      extract data from html code:
           - votes (number)
           - answer (number)
           - views (number)
           - question's text (str)
           - tags (list)
      and create the json format
     """
     data = re.search(
               '<div class="question-summary narrow"\s*id="question-summary-([0-9]+)"\s*> '+
               '.*?'+
               '<span title="[0-9]+\s*vote[s]?">\s*([0-9]+)\s*</span>\s*'+
               '.*?'+
               '<span title="[0-9]+\s*answer[s]?">\s*([0-9]+)\s*</span>\s*'+
               '.*?'+
               '<span title="[0-9]+\s*view[s]?">\s*([0-9]+)\s*</span>\s*'+
               '.*?'+
               '<h3>\s*<a href=".+?"\s*class="question-hyperlink"\s*title=".*?"\s*>(.*)</a>\s*</h3>'+
               '.*?'+
               '<div class="tags .*?">(.*)</div>'
               ,match, re.U)

     if data != None:
          data_json = dict()
          data_json['id_question'] = data.group(1)
          data_json['votes'] = int(data.group(2))
          data_json['answers'] = int(data.group(3))
          data_json['views'] = int(data.group(4))
          data_json['question'] = data.group(5)
          data_json['tags'] = find_all_tags(data.group(6))
          data_json['timestamp'] = str(datetime.datetime.now())

          return data_json
     else:
          return None

def find_all_tags(html):
     """
      find all tags related to the question
     """
     return re.findall('<a href=".*?" class="post-tag" title=".*?" rel="tag">(?:<img src=".*?" height="16" width="18" alt=".*?" class="sponsor-tag-img">)?(.*?)</a>'
                       ,html, re.U)

if __name__ == '__main__':

     html_code = fetch_page() # fetch html page from the SITE stackoverflow.com

     questions = parse_html(html_code) # parse html and create json format

     started_time = datetime.datetime.now()
     for question in questions:
          print json.dumps(question, sort_keys=True, indent=4, separators=(',',': '))
          print
     ended_time = datetime.datetime.now()
     
     print 'Summary\n======='
     print 'Questions  : %d'%len(questions)
     print 'Started at : %s'%str(started_time)
     print 'Ended at   : %s'%str(ended_time)



