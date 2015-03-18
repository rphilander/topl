# Topl

## Overview

Topl is a programming language for orchestrating heterogenous services on a network. A Topl program interacts with web services, databases, search engines, message queues, key-value stores, etc., and provides the logic and data transformations necessary to connect these services to each other as desired.

Topl makes it easy to build systems emphasizing following qualities:

* resilient, long-running
* throughput, concurrency
* visibility into system state, real-time and historical
* ease of deployment
* ease of starting, pausing, restarting, graceful shutdown, aborting

Topl is explicitly **not** intended for building systems which are stateful (i.e. data stores) or systems which carry out complex and/or expensive computations.

## Hello World

```
"Hello, world!" -> @stdout
```

