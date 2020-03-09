import * as echarts from '../../ec-canvas/echarts';
import * as china from '../../ec-canvas/china.js';

let chart = null;

// 2、进行初始化数据
function initChart(canvas, width, height) {
  chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);
  
  var optionMap = {
    backgroundColor: '#FFFFFF',
    title: {
      text: '',
      subtext: '',
      x: 'center',
      textStyle: {
        fontSize: 12,
      },
    },
    tooltip: {
      trigger: 'item',
      formatter: function (params, ticket, callback) {
        return params.seriesName + '\n' + params.name + '：' + params.value
      }
      // formatter: '{b}', //提示标签格式
      // backgroundColor: "#ff7f50",//提示标签背景颜色
      // textStyle: { color: "#fff" } //提示标签字体颜色
    },

    //左侧小导航图标
    visualMap: {
      show: true,
      x: 'left',
      y: 'bottom',
      textStyle:{
        fontSize:8,
      },
      splitList: [
        { start: 1, end: 9 }, { start: 10, end: 99 },
        { start: 100, end: 999 }, { start: 1000, end: 9999 },
        { start: 10000 }
      ],
      color: ['#8A3310', '#C64918', '#E55B25', '#F2AD92', '#F9DCD1']
    },

    //配置属性
    series: [{
      name: '累计确诊人数',
      type: 'map',
      mapType: 'china',
      zoom:1.2,
      roam: false,
      itemStyle: {
        normal: {
          borderWidth: .2,//区域边框宽度
          borderColor: '#009fe8',//区域边框颜色
          areaColor: "#ffefd5",//区域颜色
        },
        emphasis: {
          borderWidth: .5,
          borderColor: '#4b0082',
          areaColor: "#fff",
        }
      },
      label: {
        normal: {
          show: true,  //省份名称
          fontSize: 6
        },
        emphasis: {
          show: true,
          fontSize: 6
        }
      },
      data: wx.getStorageSync("key")  //数据
    }]
  };


  chart.setOption(optionMap);
  return chart;
}

function initChart2(canvas, width, height) {
  chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);

  var option2 = {
    title: {
      text: '',
      left: "left"
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type:"line",
        lineStyle: {
          color: "#7171C6"
        }
      }
    },
    legend: {
      data: ['累计确诊', '现有疑似', '累计治愈', '累计死亡'],
      // left: "right"
    },
    grid: {
      left: '3%',
      right: '5%',
      bottom: '3%',
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: wx.getStorageSync("lj").day
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '累计确诊',
        type: 'line',
        smooth: true,
        data: wx.getStorageSync("lj").confirm
      },
      {
        name: '现有疑似',
        type: 'line',
        smooth: true,
        data: wx.getStorageSync("lj").suspect
      },
      {
        name: '累计治愈',
        type: 'line',
        smooth: true,
        data: wx.getStorageSync("lj").heal
      },
      {
        name: '累计死亡',
        type: 'line',
        smooth: true,
        data: wx.getStorageSync("lj").dead
      },

    ]
  };


  chart.setOption(option2);
  return chart;
}
function initChart3(canvas, width, height) {
  chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);

  var option3 = {
    title: {
      text: '',
      left: "left"
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: "line",
        lineStyle: {
          color: "#7171C6"
        }
      }
    },
    legend: {
      data: ['新增确诊', '新增疑似'],
      // left: "right"
    },
    grid: {
      left: '3%',
      right: '5%',
      bottom: '3%',
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: wx.getStorageSync("xz").day
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '新增确诊',
        type: 'line',
        smooth: true,
        data: wx.getStorageSync("xz").confirm_add
      },
      {
        name: '新增疑似',
        type: 'line',
        smooth: true,
        data: wx.getStorageSync("xz").suspect_add
      },

    ]
  };


  chart.setOption(option3);
  return chart;
}

Page({
  onShareAppMessage: function (res) {
    return {
      title: '点击查看全国疫情',
      path: '/pages/index/index',
      success: function () { },
      fail: function () { }
    }
  },
  data: {
    time: "",
    ec: {
      onInit: initChart // 3、将数据放入到里面
    },
    ec2: {
      onInit: initChart2 // 3、将数据放入到里面
    },
    ec3: {
      onInit: initChart3 // 3、将数据放入到里面
    }
  },
  onShow: function () {
    // var lists = wx.getStorageSync('txt')
    let that = this
    wx.request({
      url: 'http://127.0.0.1:5000/time/',
      method: "get",
      success(res) {
        // console.log(res)
        that.setData({       
          time: res.data.data.time,
          confirm: res.data.data.confirm,
          suspect: res.data.data.suspect,
          heal: res.data.data.heal,
          dead: res.data.data.dead
        })
      }
    }),
      
      wx.request({
        url: 'http://127.0.0.1:5000/china/',
        method: "get",
        success(res) {
          wx.setStorageSync('key', res.data.data)        
        }
      }),
      wx.request({
        url: 'http://127.0.0.1:5000/lj/',
        method: "get",
        success(res) {
          wx.setStorageSync('lj', res.data)
        }
      }),
      wx.request({
        url: 'http://127.0.0.1:5000/xz/',
        method: "get",
        success(res) {
          wx.setStorageSync('xz', res.data)
        }
      })


  },

  onReady() {
    setTimeout(function () {
      // 获取 chart 实例的方式
      console.log(chart)
    }, 2000);
  }
});
