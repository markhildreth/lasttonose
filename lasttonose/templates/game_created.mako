<%inherit file="/base.mako"/>

<%def name="content()">
    <h2>Game Created!</h2>
    <p>The game to decide who will ${game['name']} has started! Share the following link with the fellow game members!</p>

    <input class="long_text" style="margin-left: 2em;" type="text" value="http://lasttonose.com${encoded_path}"/>

    <p>Next, you can <a href="${encoded_path}">click this link to touch your nose so you don't have to do it!</p>
</%def>

