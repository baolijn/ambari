#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
from ambari_commons import OSConst
from service_mapping import *
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
import glob

@OsFamilyFuncImpl(os_family=OSConst.WINSRV_FAMILY)
def ams(name=None):
  import params
  if name == 'collector':
    if not check_windows_service_exists(collector_win_service_name):
      Execute(format("cmd /C cd {ams_collector_home_dir} & ambari-metrics-collector.cmd setup"))

    Directory(params.ams_collector_conf_dir,
              owner=params.ams_user,
              recursive=True
    )

    Directory(params.ams_checkpoint_dir,
              owner=params.ams_user,
              recursive=True
    )

    XmlConfig("ams-site.xml",
              conf_dir=params.ams_collector_conf_dir,
              configurations=params.config['configurations']['ams-site'],
              configuration_attributes=params.config['configuration_attributes']['ams-site'],
              owner=params.ams_user,
    )

    XmlConfig( "hbase-site.xml",
               conf_dir = params.ams_collector_conf_dir,
               configurations = params.config['configurations']['ams-hbase-site'],
               configuration_attributes=params.config['configuration_attributes']['ams-hbase-site'],
               owner = params.ams_user,
    )

    if (params.log4j_props != None):
      File(os.path.join(params.ams_collector_conf_dir, "log4j.properties"),
           owner=params.ams_user,
           content=params.log4j_props
      )

    File(os.path.join(params.ams_collector_conf_dir, "ams-env.cmd"),
         owner=params.ams_user,
         content=InlineTemplate(params.ams_env_sh_template)
    )

    pass

  elif name == 'monitor':
    if not check_windows_service_exists(monitor_win_service_name):
      Execute(format("cmd /C cd {ams_monitor_home_dir} & ambari-metrics-monitor.cmd setup"))

    # creating symbolic links on ams jars to make them available to services
    links_pairs = [
      ("%HADOOP_HOME%\\share\\hadoop\\common\\lib\\ambari-metrics-hadoop-sink-with-common.jar",
       "%SINK_HOME%\\hadoop-sink\\ambari-metrics-hadoop-sink-with-common-*.jar"),
      ("%HBASE_HOME%\\lib\\ambari-metrics-hadoop-sink-with-common.jar",
       "%SINK_HOME%\\hadoop-sink\\ambari-metrics-hadoop-sink-with-common-*.jar"),
    ]
    for link_pair in links_pairs:
      link, target = link_pair
      target = glob.glob(os.path.expandvars(target))[0].replace("\\\\", "\\")
      Execute('cmd /c mklink "{0}" "{1}"'.format(link, target))

    Directory(params.ams_monitor_conf_dir,
              owner=params.ams_user,
              recursive=True
    )

    TemplateConfig(
      os.path.join(params.ams_monitor_conf_dir, "metric_monitor.ini"),
      owner=params.ams_user,
      template_tag=None
    )

    TemplateConfig(
      os.path.join(params.ams_monitor_conf_dir, "metric_groups.conf"),
      owner=params.ams_user,
      template_tag=None
    )

@OsFamilyFuncImpl(os_family=OsFamilyImpl.DEFAULT)
def ams(name=None):
  import params

  if name == 'collector':
    Directory(params.ams_collector_conf_dir,
              owner=params.ams_user,
              group=params.user_group,
              recursive=True
    )

    Directory(params.ams_checkpoint_dir,
              owner=params.ams_user,
              group=params.user_group,
              recursive=True
    )

    XmlConfig("ams-site.xml",
              conf_dir=params.ams_collector_conf_dir,
              configurations=params.config['configurations']['ams-site'],
              configuration_attributes=params.config['configuration_attributes']['ams-site'],
              owner=params.ams_user,
              group=params.user_group
    )

    XmlConfig( "hbase-site.xml",
               conf_dir = params.ams_collector_conf_dir,
               configurations = params.config['configurations']['ams-hbase-site'],
               configuration_attributes=params.config['configuration_attributes']['ams-hbase-site'],
               owner = params.ams_user,
               group = params.user_group
    )

    if (params.log4j_props != None):
      File(format("{params.ams_collector_conf_dir}/log4j.properties"),
           mode=0644,
           group=params.user_group,
           owner=params.ams_user,
           content=params.log4j_props
      )

    File(format("{ams_collector_conf_dir}/ams-env.sh"),
         owner=params.ams_user,
         content=InlineTemplate(params.ams_env_sh_template)
    )

    Directory(params.ams_collector_log_dir,
              owner=params.ams_user,
              group=params.user_group,
              recursive=True
    )

    Directory(params.ams_collector_pid_dir,
              owner=params.ams_user,
              group=params.user_group,
              recursive=True
    )

    pass

  elif name == 'monitor':
    Directory(params.ams_monitor_conf_dir,
              owner=params.ams_user,
              group=params.user_group,
              recursive=True
    )

    Directory(params.ams_monitor_log_dir,
              owner=params.ams_user,
              group=params.user_group,
              recursive=True
    )

    Directory(params.ams_monitor_pid_dir,
              owner=params.ams_user,
              group=params.user_group,
              recursive=True
    )

    Directory(format("{ams_monitor_dir}/psutil/build"),
              owner=params.ams_user,
              group=params.user_group,
              recursive=True)

    TemplateConfig(
      format("{ams_monitor_conf_dir}/metric_monitor.ini"),
      owner=params.ams_user,
      group=params.user_group,
      template_tag=None
    )

    TemplateConfig(
      format("{ams_monitor_conf_dir}/metric_groups.conf"),
      owner=params.ams_user,
      group=params.user_group,
      template_tag=None
    )

    File(format("{ams_monitor_conf_dir}/ams-env.sh"),
         owner=params.ams_user,
         content=InlineTemplate(params.ams_env_sh_template)
    )

    # TODO
    pass

  pass
