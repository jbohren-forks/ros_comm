#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

PKG = 'test_roslaunch'

import os, sys, unittest

import xmlrpclib
import rostest
import rospkg

import rosgraph
master = rosgraph.Master('conditionals')
def get_param(*args):
    return master.getParam(*args)
    
## Test Roslaunch 'param' tags
class TestConditionals(unittest.TestCase):

    ## test simple constant values
    def test_simple(self):
        true_param_keys = ['ti1', 'tu1', 'ti2', 'tu2']
        for k in true_param_keys:
            self.assertEquals(get_param('conditionals/simple/'+k), k)

        params = get_param('conditionals/simple')
        for k, v in params.items():
            self.assertFalse(k[0] == 'f')

    ## test arguments
    def test_arguments(self):
        true_param_keys = ['ti1', 'tu1']
        for k in true_param_keys:
            self.assertEquals(get_param('conditionals/arguments/'+k), k)

        params = get_param('conditionals/arguments')
        for k, v in params.items():
            self.assertFalse(k[0] == 'f')

      ## test boolean operations
      def test_bool_operations(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'tu2', 'ti3', 'tu3', 'ti4', 'tu4', 'ti5', 
                  'tu5', 'ti6', 'tu6', 'ti7', 'tu7', 'ti8', 'tu8', 'ti9', 'tu9', 'ti10', 
                  'tu10', 'ti11', 'tu11']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/bool_operations/'+k), k)                     
                                                                                               
          params = get_param('conditionals/bool_operations')                                                  
              self.assertFalse(k[0] == 'f')

    ## test boolean operations with arguments
      def test_bool_operations_arg(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'tu2', 'ti3', 'tu3', 'ti4', 'tu4', 'ti5', 
                  'tu5', 'ti6', 'tu6', 'ti7', 'tu7', 'ti8', 'tu8', 'ti9', 'tu9', 'ti10', 
                  'tu10', 'ti11', 'tu11']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/bool_operations_arg/'+k), k)                     
                                                                                               
          params = get_param('conditionals/bool_operations_arg')                                                  
              self.assertFalse(k[0] == 'f')

      ## test built in functions
      def test_built_ins(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'tu2', 'ti3', 'ti4', 'ti5', 'ti6', 'ti7', 
                  'ti8', 'ti9', 'ti10']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/built_ins/'+k), k)                     
                                                                                               
          params = get_param('conditionals/built_ins')                                                  
              self.assertFalse(k[0] == 'f')

      ## test built in functions with arguments
      def test_built_ins_arg(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'tu2', 'ti3', 'ti4', 'ti5', 'ti6', 'ti7', 
                  'ti8', 'ti9', 'ti10']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/built_ins_arg/'+k), k)                     
                                                                                               
          params = get_param('conditionals/built_ins_arg')                                                  
              self.assertFalse(k[0] == 'f')

    ## test built in functions with bool operators
      def test_built_ins_bool(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'tu2', 'ti3', 'tu3', 'ti4', 'tu4', 'ti5', 
                  'tu5']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/built_ins_bool/'+k), k)                     
                                                                                               
          params = get_param('conditionals/built_ins_bool')                                                  
              self.assertFalse(k[0] == 'f')

    ## test built in functions with bool operators and arguments
      def test_built_ins_bool_arg(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'tu2', 'ti3', 'tu3', 'ti4', 'tu4', 'ti5', 
                  'tu5']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/built_ins_bool_arg/'+k), k)                     
                                                                                               
          params = get_param('conditionals/built_ins_bool_arg')                                                  
              self.assertFalse(k[0] == 'f')

    ## test math
      def test_math(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'ti3', 'ti4', 'ti5', 'ti6', 'ti7', 'ti8', 
                  'ti9', 'ti10', 'ti11', 'ti12', 'ti13', 'ti14', 'ti15', 'ti16', 'ti17', 
                  'ti18', 'ti19']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/math/'+k), k)                     
                                                                                               
          params = get_param('conditionals/math')                                                  
              self.assertFalse(k[0] == 'f')

    ## test math with arguments
      def test_math_arg(self):                                                                
          true_param_keys = ['ti1', 'tu1', 'ti2', 'ti3', 'ti4', 'ti5', 'ti6', 'ti7', 'ti8', 
                  'ti9', 'ti10', 'ti11', 'ti12', 'ti13', 'ti14', 'ti15', 'ti16', 'ti17', 
                  'ti18', 'ti19']
          for k in true_param_keys:                                                            
              self.assertEquals(get_param('conditionals/math_arg/'+k), k)                     
                                                                                               
          params = get_param('conditionals/math_arg')                                                  
              self.assertFalse(k[0] == 'f')

if __name__ == '__main__':
    rostest.rosrun(PKG, sys.argv[0], TestConditionals, sys.argv)
    
