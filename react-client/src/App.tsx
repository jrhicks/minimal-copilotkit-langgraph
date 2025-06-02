import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { CopilotKit } from '@copilotkit/react-core'
import { CopilotSidebar } from '@copilotkit/react-ui'
import '@copilotkit/react-ui/styles.css'
import { useCopilotAction } from '@copilotkit/react-core'

function CounterCard() {
  const [count, setCount] = useState(0)

  useCopilotAction({
    name: "incrementCounter",
    description: "Increment the counter in the UI.",
    available: "remote",
    handler: async () => {
      setCount((c) => c + 1)
    },
  })

  return (
    <div className="p-8 rounded-xl bg-neutral-800 shadow-md flex flex-col items-center gap-4 my-6">
      <button
        className="rounded-lg border border-neutral-700 px-6 py-2 text-lg font-semibold bg-neutral-900 text-white hover:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors"
        onClick={() => setCount((count) => count + 1)}
      >
        count is {count}
      </button>
      <p className="text-neutral-400">
        Edit <code className="bg-neutral-700 text-white px-1 rounded">src/App.tsx</code> and save to test HMR
      </p>
    </div>
  )
}

function App() {
  return (
    <CopilotKit
      runtimeUrl="http://localhost:4000/copilotkit"
      agent="sample_agent"
    >
      <CopilotSidebar
        defaultOpen={false}
        instructions={"You are assisting the user as best as you can. Answer in the best way possible given the data you have."}
        labels={{
          title: "Sidebar Assistant",
          initial: "How can I help you today?",
        }}
      >
        <div className="min-h-screen w-full max-w-3xl mx-auto p-8 text-center flex flex-col items-center justify-center bg-neutral-900 text-white">
          <div className="flex gap-8 justify-center mb-6">
            <a href="https://vite.dev" target="_blank" rel="noopener noreferrer">
              <img src={viteLogo} className="h-24 w-24 p-6 transition-filter duration-300 hover:drop-shadow-[0_0_2em_#646cffaa]" alt="Vite logo" />
            </a>
            <a href="https://react.dev" target="_blank" rel="noopener noreferrer">
              <img src={reactLogo} className="h-24 w-24 p-6 transition-filter duration-300 hover:drop-shadow-[0_0_2em_#61dafbaa]" alt="React logo" />
            </a>
          </div>
          <h1 className="text-5xl font-bold mb-4">Vite + React</h1>
          <CounterCard />
          <p className="text-neutral-400 mt-8">
            Click on the Vite and React logos to learn more
          </p>
        </div>
      </CopilotSidebar>
    </CopilotKit>
  )
}

export default App
