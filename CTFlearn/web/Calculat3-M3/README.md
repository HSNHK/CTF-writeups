# Calculat3 M3

A simple command injection challenge will be demonstrated in this walkthrough

Here is the challenge page we got after visiting the given link.

I provided random input in this calculator and intercepted the request with BurpSuite

I got one parameter `expression` taking the values 
```
expression: 8 5 * 6 6 
```
`;ls` was used to try to inject commands

After forwarding the request above, it has finally been flagged

```
ctf{*****_***_***_***_*********}
```