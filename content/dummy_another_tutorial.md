---
title: "Tutorial: Advanced Python Scripting for Pentesters"
date: "2026-02-15"
category: "Tutorial"
tags: "Python, Advanced, Pentesting"
description: "Lanjutan dari tutorial sebelumnya, kita akan membahas teknik threading dan async di Python untuk mempercepat scanning."
---

![Python Advanced](../assets/img/test_image.png)

## Overview

Setelah menguasai dasar-dasar, saatnya beralih ke teknik yang lebih advanced. Dalam tutorial ini kita akan membahas:

1.  **Multi-threading**: Agar script jalan paralel.
2.  **AsyncIO**: Alternatif ringan untuk concurrency.
3.  **Argparse**: Membuat command line argument yang profesional.

## Multi-threading

Contoh code sederhana:

```python
import threading

def worker(num):
    print(f"Worker {num} is working")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
```

Keep hacking!
