
totp_sync_template = '''
<!DOCTYPE html>
<html>
<body>
<canvas id="qr"></canvas>

<script src="https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js"></script>
<script>
  (function () {
    var qr = new QRious({
      element: document.getElementById('qr'),
      value: '%s'
    });
  })();
</script>
<p>Scan QR-code with TOTP-app and input code</p>
<form method="post" action="?user_id=%s">
    <input required name="code">
    <button type="submit">Synchronising</button>
</form>
</body>
</html>
'''

check_totp_tmpl = '''
<!DOCTYPE html>
<html>
<body>
<p>{message}</p>
<p>Input your code from TOTP-app</p>
<form method="post" action="?user_id={user_id}">
    <input required name="code">
    <button type="submit">Synchronising</button>
</form>
</body>
</html>
'''