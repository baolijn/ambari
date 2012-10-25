/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

var App = require('app');

/**
 * @class
 * 
 * This is a view for showing cluster load
 * 
 * @extends App.ChartLinearTimeView
 * @extends Ember.Object
 * @extends Ember.View
 */
App.ChartClusterMetricsLoad = App.ChartLinearTimeView.extend({
  id: "cluster-metrics-load",
  url: "/data/cluster_metrics/load_1hr.json",
  title: "Cluster Load",
  
  transformToSeries: function(jsonData){
    var seriesArray = [];
    if(jsonData instanceof Array){
      jsonData.forEach(function(data){
        var series = {};
        series.name = data.metric_name;
        series.data = [];
        for(var index=0; index<data.datapoints.length; index++){
          series.data.push({
            x: data.datapoints[index][1],
            y: data.datapoints[index][0]
          });
        }
        seriesArray.push(series);
      });
    }
    return seriesArray;
  }
});