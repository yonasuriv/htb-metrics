# HTB Metrics Badge Generator

Currently in the alpha stage. Keep an eye out for upcoming templates and updates, or contribute to the development!

<!--header-->
<table>
  <tr><td colspan="2"></td></tr>
  <tr><th colspan="2"><h3>📗 Classic Badge</h3></th></tr>
  <tr><td colspan="2" align="center"><p>Default Template.</p>
</td></tr>
  <tr>
    <th rowspan="3">Supported features<br></th>
    <td></td>
  </tr>
  <tr>
    <td><code>👤 User</code></td>
  </tr>
  <tr>
    <td><code>*️⃣ PNG</code></td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="https://github.com/user-attachments/assets/b7ad88f4-0ca5-4721-95a2-d125ab780dcf" alt=""></img>
      <img width="950" height="1" alt="">
    </td>
  </tr>
</table>
<!--/header-->

## ℹ️ Examples workflows

<!--examples-->
```yaml
name: Example
uses: yonasuriv/htb-metrics@latest
with:
  filename: htb-metrics.classic.png
  token: ${{ secrets.HTB-METRICS_TOKEN }}
  base: header, repositories
```
<!--/examples-->
