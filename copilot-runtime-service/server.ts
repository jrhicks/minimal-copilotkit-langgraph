import { createServer } from 'node:http';
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNodeHttpEndpoint,
} from '@copilotkit/runtime';


const serviceAdapter = new ExperimentalEmptyAdapter();

const server = createServer((req, res) => {
  const runtime = new CopilotRuntime({
    remoteEndpoints: [
      { url: "http://localhost:8000/copilotkit" },
    ],
  });

  const handler = copilotRuntimeNodeHttpEndpoint({
    endpoint: '/copilotkit',
    runtime,
    serviceAdapter,
  });

  return handler(req, res);
});

server.listen(4000, () => {
  console.log('Listening at http://localhost:4000/copilotkit');
});