"""Run golden questions against the API and print accuracy + latency."""
import json, time, httpx

CASES = json.load(open(__file__.replace("run_evals.py", "golden.json")))
ok, t0 = 0, time.time()
for c in CASES:
    r = httpx.post("http://localhost:8000/ask", json={"question": c["q"]}, timeout=120).json()
    hit = r["status"] == c["expect_status"] and all(k.lower() in r["answer"].lower() for k in c.get("keywords", []))
    ok += hit
    print(("PASS" if hit else "FAIL"), c["q"])
print(f"accuracy {ok}/{len(CASES)}  avg latency {(time.time()-t0)/len(CASES):.1f}s")
