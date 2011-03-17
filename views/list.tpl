%from urllib import quote
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Bottle + MongoDB Example</title>
    <link type="text/css" href="/static/css/main.css" rel="stylesheet">
    <script type="text/javascript">
      function toggle(id) {
        var el = document.getElementById(id);
        el.style.display = (el.style.display != 'none' ? 'none' : '' );
      }
    </script>
  </head>
  <body>
    <h1>Bottle + MongoDB Example</h1>
    <h2>New message</h2>
    <form action="/create" method="POST" enctype="multipart/form-data">
      <table>
        <tr>
          <td>Message:</td>
          <td><textarea rows="3" name="text"></textarea></td>
        </tr>
        <tr>
          <td>Nickname:</td>
          <td><input type="text" name="nickname"></td>
        </tr>
        <tr>
          <td>Image:</td>
          <td>
            <input type="file" name="image">
          </td>
        </tr>
        <tr>
          <td></td>
          <td>
            <input type="submit" value="Create New Message" onclick="toggle('spinner');">
            <img src="/static/images/spinner.gif" id="spinner" style="display: none;">
          </td>
        </tr>
      </table>
    </form>
    <h2>Messages</h2>
    <table id="messages">
    %for message in messages:
      <tr>
        <td class="thumb">
          %if 'image' in message:
          <a href="/images/{{quote(message['image'])}}">
            <img src="/thumbs/{{quote(message['image'])}}" alt="">
          </a>
          %end
        </td>
        <td class="nickname">
          {{message['nickname']}}
        </td>
        <td class="text">
          {{message['text']}}
        </td>
        <td class="date">
          {{message['date'].strftime('%X %d %b %y')}}
        </td>
      </tr>
    %end
    </table>
    <div id="navigation">
      %if prev_page is not None:
      <a href="/list/{{prev_page}}">&lt; Prev</a>
      %end
      %if next_page is not None:
      <a href="/list/{{next_page}}">Next &gt;</a>
      %end
    </div>
    <div id="poweredby">
      <img src="/static/images/poweredby.png" alt="Powered by Bottle + MongoDB">
    </div>
  </body>
</html>

