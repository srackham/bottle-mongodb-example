## list.html
<%inherit file="base.mako"/>

<%!
  title = 'Bottle + MongoDB Example'
%>

## Start body.
<h2>New message</h2>
${self.create_form()}
<h2>Messages</h2>
${self.messages_table()}
${self.footer()}
## End body.

<%def name="create_form()">
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
</%def>

<%def name="messages_table()">
  <table id="messages">
  %for message in messages:
    <tr>
      <td class="thumb">
        %if message.has_image():
        <a href="/image/${message.image_id()}">
          <img src="/image/${message.thumb_id()}" alt="">
        </a>
        %endif
      </td>
      <td class="nickname">
        ${message['nickname']}
      </td>
      <td class="text">
        ${message['text']}
      </td>
      <td class="date">
        ${message['date'].strftime('%X %d %b %y')}
      </td>
    </tr>
  %endfor
  </table>
</%def>

<%def name="footer()">
  <div id="navigation">
    %if prev_page is not None:
    <a href="/list/${prev_page}">&lt; Prev</a>
    %endif
    %if next_page is not None:
    <a href="/list/${next_page}">Next &gt;</a>
    %endif
  </div>
  <div id="poweredby">
    <img src="/static/images/poweredby.png" alt="Powered by Bottle + MongoDB">
  </div>
</%def>
