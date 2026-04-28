import { useEffect, useState } from 'react'

interface ProviderItem {
  id: string
  name: string
  provider: string
  apiKey: string
  model: string
  baseUrl?: string
  notes?: string
  active?: boolean
}

export default function Home() {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([])
  const [input, setInput] = useState('')
  const [novels, setNovels] = useState<Array<any>>([])
  const [providers, setProviders] = useState<ProviderItem[]>([])
  const [selectedNovel, setSelectedNovel] = useState<any>(null)
  const [currentView, setCurrentView] = useState<'chat' | 'novels' | 'settings'>('chat')
  const [editingProvider, setEditingProvider] = useState<ProviderItem | null>(null)
  const [providerForm, setProviderForm] = useState({
    name: '',
    provider: 'openai',
    apiKey: '',
    model: 'gpt-4o',
    baseUrl: '',
    notes: ''
  })

  useEffect(() => {
    if (currentView === 'novels') {
      fetchNovels()
    }
    if (currentView === 'settings') {
      fetchProviders()
    }
  }, [currentView])

  const fetchNovels = async () => {
    try {
      const response = await fetch('/api/novels')
      const data = await response.json()
      setNovels(data)
    } catch (error) {
      console.error('Error fetching novels:', error)
    }
  }

  const fetchProviders = async () => {
    try {
      const response = await fetch('/api/providers')
      const data = await response.json()
      setProviders(data)
    } catch (error) {
      console.error('Error fetching providers:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })
      const data = await response.json()
      const aiMessage = { role: 'ai', content: data.response }
      setMessages(prev => [...prev, aiMessage])
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const resetProviderForm = () => {
    setEditingProvider(null)
    setProviderForm({
      name: '',
      provider: 'openai',
      apiKey: '',
      model: 'gpt-4o',
      baseUrl: '',
      notes: ''
    })
  }

  const handleProviderSave = async () => {
    const payload = {
      ...providerForm,
      baseUrl: providerForm.baseUrl || undefined,
      notes: providerForm.notes || undefined
    }

    try {
      if (editingProvider) {
        await fetch(`/api/providers/${editingProvider.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
      } else {
        await fetch('/api/providers', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
      }
      await fetchProviders()
      resetProviderForm()
    } catch (error) {
      console.error('Error saving provider:', error)
    }
  }

  const handleProviderActivate = async (providerId: string) => {
    try {
      await fetch(`/api/providers/${providerId}/activate`, {
        method: 'POST'
      })
      await fetchProviders()
    } catch (error) {
      console.error('Error activating provider:', error)
    }
  }

  const handleProviderDelete = async (providerId: string) => {
    try {
      await fetch(`/api/providers/${providerId}`, {
        method: 'DELETE'
      })
      await fetchProviders()
    } catch (error) {
      console.error('Error deleting provider:', error)
    }
  }

  const handleProviderEdit = (provider: ProviderItem) => {
    setEditingProvider(provider)
    setProviderForm({
      name: provider.name,
      provider: provider.provider,
      apiKey: provider.apiKey,
      model: provider.model,
      baseUrl: provider.baseUrl || '',
      notes: provider.notes || ''
    })
  }

  const renderContent = () => {
    switch (currentView) {
      case 'chat':
        return (
          <div className="flex-1 flex flex-col">
            <div className="flex-1 overflow-y-auto p-4">
              {messages.map((msg, idx) => (
                <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-white text-black'}`}>
                    {msg.content}
                  </div>
                </div>
              ))}
            </div>
            <div className="p-4 border-t">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                  className="flex-1 p-2 border rounded-l"
                  placeholder="输入您的消息..."
                />
                <button onClick={sendMessage} className="px-4 py-2 bg-blue-500 text-white rounded-r">
                  发送
                </button>
              </div>
            </div>
          </div>
        )
      case 'novels':
        return (
          <div className="flex-1 p-4 overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">小说仓库</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {novels.map((novel) => (
                <div key={novel.id} className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-semibold">{novel.title}</h3>
                  <p className="text-gray-600">作者: {novel.author}</p>
                  <p className="text-gray-600">类型: {novel.genre}</p>
                  <p className="text-sm text-gray-500 mt-2">{novel.summary}</p>
                  <button
                    onClick={() => setSelectedNovel(novel)}
                    className="mt-3 inline-flex items-center px-3 py-1 bg-blue-500 text-white rounded"
                  >
                    查看详情
                  </button>
                </div>
              ))}
            </div>
            {selectedNovel && (
              <div className="mt-8 bg-white p-4 rounded-lg shadow">
                <h3 className="text-xl font-bold">{selectedNovel.title}</h3>
                <p className="text-gray-600">作者: {selectedNovel.author}</p>
                <div className="mt-4 whitespace-pre-wrap text-gray-800">{selectedNovel.content}</div>
                <button
                  onClick={() => setSelectedNovel(null)}
                  className="mt-4 px-3 py-1 bg-gray-500 text-white rounded"
                >
                  关闭
                </button>
              </div>
            )}
          </div>
        )
      case 'settings':
        return (
          <div className="flex-1 p-4 overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">设置</h2>
            <div className="grid grid-cols-1 lg:grid-cols-[360px_minmax(0,1fr)] gap-6">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-3">模型提供商</h3>
                <div className="space-y-3">
                  {providers.map((provider) => (
                    <div key={provider.id} className="rounded-lg border p-3">
                      <div className="flex items-center justify-between gap-2">
                        <div>
                          <div className="font-semibold">{provider.name}</div>
                          <div className="text-sm text-gray-500">{provider.provider} / {provider.model}</div>
                        </div>
                        <div className="flex items-center gap-2">
                          {provider.active && <span className="px-2 py-1 text-xs text-white bg-green-500 rounded">已激活</span>}
                          <button onClick={() => handleProviderActivate(provider.id)} className="text-sm text-blue-600">激活</button>
                          <button onClick={() => handleProviderEdit(provider)} className="text-sm text-gray-600">编辑</button>
                          <button onClick={() => handleProviderDelete(provider.id)} className="text-sm text-red-600">删除</button>
                        </div>
                      </div>
                      <div className="text-xs text-gray-500 mt-2">{provider.notes}</div>
                    </div>
                  ))}
                  {providers.length === 0 && <div className="text-gray-500">还没有配置模型提供商，您可以添加一个。</div>}
                </div>
              </div>

              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-3">添加 / 编辑提供商</h3>
                <div className="space-y-3">
                  <label className="block">
                    <div className="text-sm font-medium mb-1">名称</div>
                    <input
                      value={providerForm.name}
                      onChange={(e) => setProviderForm({ ...providerForm, name: e.target.value })}
                      className="w-full border rounded px-3 py-2"
                    />
                  </label>
                  <label className="block">
                    <div className="text-sm font-medium mb-1">提供商类型</div>
                    <select
                      value={providerForm.provider}
                      onChange={(e) => setProviderForm({ ...providerForm, provider: e.target.value })}
                      className="w-full border rounded px-3 py-2"
                    >
                      <option value="openai">OpenAI</option>
                      <option value="anthropic">Anthropic</option>
                      <option value="alibaba">Alibaba</option>
                    </select>
                  </label>
                  <label className="block">
                    <div className="text-sm font-medium mb-1">API Key</div>
                    <input
                      value={providerForm.apiKey}
                      onChange={(e) => setProviderForm({ ...providerForm, apiKey: e.target.value })}
                      className="w-full border rounded px-3 py-2"
                    />
                  </label>
                  <label className="block">
                    <div className="text-sm font-medium mb-1">模型名称</div>
                    <input
                      value={providerForm.model}
                      onChange={(e) => setProviderForm({ ...providerForm, model: e.target.value })}
                      className="w-full border rounded px-3 py-2"
                    />
                  </label>
                  <label className="block">
                    <div className="text-sm font-medium mb-1">Base URL（可选）</div>
                    <input
                      value={providerForm.baseUrl}
                      onChange={(e) => setProviderForm({ ...providerForm, baseUrl: e.target.value })}
                      className="w-full border rounded px-3 py-2"
                      placeholder="例如自定义 OpenAI 或 Anthropic Endpoint"
                    />
                  </label>
                  <label className="block">
                    <div className="text-sm font-medium mb-1">备注</div>
                    <textarea
                      value={providerForm.notes}
                      onChange={(e) => setProviderForm({ ...providerForm, notes: e.target.value })}
                      className="w-full border rounded px-3 py-2"
                      rows={3}
                    />
                  </label>
                  <div className="flex gap-2">
                    <button onClick={handleProviderSave} className="px-4 py-2 bg-blue-500 text-white rounded">
                      {editingProvider ? '保存修改' : '添加提供商'}
                    </button>
                    <button onClick={resetProviderForm} className="px-4 py-2 bg-gray-200 text-gray-800 rounded">
                      重置
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-64 bg-white shadow-lg">
        <div className="p-4">
          <h2 className="text-xl font-bold">Nature AI</h2>
          <nav className="mt-4">
            <ul>
              <li className="mb-2">
                <button
                  onClick={() => setCurrentView('chat')}
                  className={`w-full text-left px-2 py-2 rounded ${currentView === 'chat' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'}`}
                >
                  对话
                </button>
              </li>
              <li className="mb-2">
                <button
                  onClick={() => setCurrentView('novels')}
                  className={`w-full text-left px-2 py-2 rounded ${currentView === 'novels' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'}`}
                >
                  小说仓库
                </button>
              </li>
              <li className="mb-2">
                <button
                  onClick={() => setCurrentView('settings')}
                  className={`w-full text-left px-2 py-2 rounded ${currentView === 'settings' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'}`}
                >
                  设置
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      {renderContent()}
    </div>
  )
}
