$(function() {
  $(document).ready(function() {
    $('#check_page').button().click(function() {
      var page = $('#page_name').val();
      console.log(page);
      // コメント中の単語の出現数を取得
      $('#error_message').empty()
      util.getJson(
        '/check_facebook/json/analyze_page/' + page,
        {},
        function (err, result) {
          if (err) {
            $('#error_message').append(err)
            return;
          }
          if (result.result) {
            $('#error_message').append(result.error)
            return;
          }

          // タグクラウド作成
          $('#termTagCloud').empty();
          $('#termTagCloud').jQCloud(result.data);
          
          // テーブルの作成
          var tbl = $('#tblTerms');
          tbl.empty();
          for (var i = 0; i < result.data.length; ++i ) {
            var tr = $('<tr/>');
            $('<td>' + result.data[i].text + '</td>').appendTo(tr);
            $('<td>' + result.data[i].weight + '</td>').appendTo(tr);
            tr.appendTo(tbl);
          }
          //$('#termTagCloud').jQCloud(result);
          //$('#termsTable').addRowData('1' , result);
        },
        function() {
          $.blockUI({ message: '<img src="/analyze_election/img/loading.gif" />' });
        },
        function() {
          $.unblockUI();
        }
      );
    });
  });
});