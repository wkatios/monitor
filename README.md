### RESTFUL API

#### URL
http://{ip:port}/api/infomations/

#### 请求方式
GET
#### 请求参数

|参数 |必填 |类型 |说明 |
| :--- | :----: | ----: |----|
|ip |否 |string |根据ip地址查询，缺省时返回全部ip信息 |
|num |否 |string |返回的记录数，缺省时返回全部记录数 |
|status |是 |string |history从全部历史数据查找，latest从最新一次数据查找 |

#### 示例

GET  http://localhost:8000/api/infomations/?status=history&ip=x.x.x.x&num=3

### 返回数据

**正确返回**

	{
	data: [
		{
		diskusagedic: {},
		memtotal: 64429,
		memusage: "12.7",
		task_zombie: "0",
		task_sleeping: "227",
		timestamp: 1509958623788,
		cpu_sy: " 0.0",
		task_stopped: "0",
		serverip: "x.x.x.x",
		swapusage: "",
		cpu_id: " 99.9",
		swaptotal: 0,
		memused: 9999,
		task_running: "1",
		conns: "955",
		processinfo: "",
		task_total: "228",
		cpu_us: " 0.1",
		swapused: 0
		},
		{...},
		{...}
	],
	result: "success",
	resmsg: "data success return"
	}

**错误返回**

	{'result': 'error', 'resmsg': 'data has not get, please check parameters'}

	{'result': 'error', 'resmsg': 'parameter is not support'}
	
#### 说明
通过GET请求获取消息，需要注意的是，status为必须参数，（latest|history)




----------
#### URL
http://{ip:port}/api/osinfo/

#### 请求方式
POST 

#### 请求参数
JSON


#### 示例
POST http://localhost:8000/api/infomations/

	data = {
			diskusagedic: {...},
			memtotal: 64429,
			memusage: "12.7",
			task_zombie: "0",
			task_sleeping: "227",
			timestamp: 1509958623788,
			cpu_sy: " 0.0",
			task_stopped: "0",
			serverip: "x.x.x.x",
			swapusage: "",
			cpu_id: " 99.9",
			swaptotal: 0,
			memused: 9999,
			task_running: "1",
			conns: "955",
			processinfo: "",
			task_total: "228",
			cpu_us: " 0.1",
			swapused: 0
			}


#### 返回数据
**正确返回**

	{'result': 'success', 'resmsg': 'data is saved'}

**错误返回**

	{'result': 'error', 'resmsg': 'data is unsaved, please check parameters'}

#### 说明
post数据格式要求json，对其中的字段未作严格限制。主要作用是上报各个机器os信息，进程信息或其他相关信息。