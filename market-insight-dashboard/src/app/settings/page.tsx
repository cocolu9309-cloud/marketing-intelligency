'use client'

export default function SettingsPage() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">设置</h2>
      <div className="bg-white border rounded-lg p-6 max-w-xl">
        <h3 className="font-medium mb-4">数据源配置</h3>
        <div className="space-y-4 text-sm">
          <div>
            <label className="block text-slate-500 mb-1">Ahrefs MCP URL</label>
            <input
              type="text"
              placeholder="http://localhost:8080/mcp"
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-slate-500 mb-1">LLM API URL</label>
            <input
              type="text"
              placeholder="http://localhost:8000/v1/chat"
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-slate-500 mb-1">扫描间隔（小时）</label>
            <input
              type="number"
              defaultValue={6}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <button className="px-4 py-2 bg-primary-500 text-white rounded hover:bg-primary-600">
            保存配置
          </button>
        </div>
      </div>
    </div>
  )
}
