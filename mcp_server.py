import sys, json
from client import AgentSemanticCacheDeduplicator

def main():
    engine = AgentSemanticCacheDeduplicator()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "get", "description": "Get from cache.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
                        {"name": "put", "description": "Put into cache.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "response": {"type": "string"}}, "required": ["query", "response"]}},
                        {"name": "get_metrics", "description": "Get metrics.", "inputSchema": {"type": "object"}},
                        {"name": "run_benchmark_semantic_cache", "description": "Run self-test.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "get":
                    out = engine.get(args.get("query", ""))
                elif tname == "put":
                    out = engine.put(args.get("query", ""), args.get("response", ""))
                elif tname == "get_metrics":
                    out = engine.get_metrics()
                elif tname == "run_benchmark_semantic_cache":
                    out = engine.run_benchmark_semantic_cache()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
