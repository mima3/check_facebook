<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Facebook OAuth Example</title>
  </head>
  <body>
    %if access_token:
      <p><a href="/check_facebook/logout">Log out</a></p>
    %else:
      <p><a href="/check_facebook/login">Log in</a></p>
    %end
    <p><a href="/check_facebook/analyze_page">Facebookページの解析</a></p>
  </body>
</html>
