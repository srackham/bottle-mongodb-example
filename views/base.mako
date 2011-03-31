## base.html
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>${self.attr.title}</title>
    <link type="text/css" href="/static/css/main.css" rel="stylesheet">
    <script type="text/javascript">
      function toggle(id) {
        var el = document.getElementById(id);
        el.style.display = (el.style.display != 'none' ? 'none' : '' );
      }
    </script>
  </head>
  <body>
    <h1>${self.attr.title}</h1>
    ${self.body()}
  </body>
</html>


