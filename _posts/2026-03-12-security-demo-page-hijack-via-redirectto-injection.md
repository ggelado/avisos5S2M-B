---
layout: post
title: "SECURITY DEMO - Page Hijack via redirect_to injection"
date: 2026-03-12 10:00:00 +0100

author: 
  name: Security Researcher
  email: test@alumnos.upm.es
published: true
expires: 2026-12-31 23:59:00 +0100
excerpt: "YAML injection: redirect_to + permalink overrides form page"
permalink: /publicarAvisos.html
redirect_to: https://example.com
---

## PoC

This post, if merged, replaces `/publicarAvisos.html` with a redirect to an attacker-controlled site.

Real attack: redirect to a phishing clone of the form page to steal `@alumnos.upm.es` credentials.

`redirect_to` is processed by the installed `jekyll-redirect-from` gem. No further plugins needed.
