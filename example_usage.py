from client import AgentSemanticCacheDeduplicator
import json

def main():
    cache = AgentSemanticCacheDeduplicator()
    res = cache.run_benchmark_semantic_cache()
    print("Agent Semantic Cache Deduplicator Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
