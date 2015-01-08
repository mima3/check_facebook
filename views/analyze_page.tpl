<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
  <title>facebookページの解析</title>
  <link rel="stylesheet" href="/check_facebook/js/jqcloud/jqcloud.css" type="text/css" />
  <link rel="stylesheet" href="/check_facebook/base.css" type="text/css" />
  <link rel="stylesheet" href="/check_facebook/js/jquery/jquery-ui.min.css" type="text/css" />
  <script type="text/javascript" src="/check_facebook/js/jquery/jquery-1.11.1.min.js"></script>
  <script type="text/javascript" src="/check_facebook/js/jquery/jquery-ui-1.10.4.min.js"></script>
  <script type="text/javascript" src="/check_facebook/js/jqcloud/jqcloud-1.0.4.min.js" ></script>
  <script type="text/javascript" src="/check_facebook/js/blockui/jquery.blockUI.js" ></script>
  <script type="text/javascript" src="/check_facebook/js/util.js" ></script>
  <script type="text/javascript" src="/check_facebook/js/analyze_page.js" ></script>
</head>
<body>
  <div id="contents">
    <h1>facebookページの解析</h1>
    <p>ページ名/ID(meで自分のニュース)：<input id="page_name" type="text" name="name" size="30" maxlength="20"></input></p>
    <p><button id="check_page">チェック</button></p>
    <div id="error_message" class="error"></div>
    <div id="page_info"></div>
    <div id="termTagCloud" style="width: 100%; height: 480px;"></div>
    <table class="normal">
      <thead>
        <th>単語</th>
        <th>出現数</th>
      </thead>
      <tbody id="tblTerms">
      </tbody>
    </table>
</body>
</html>
