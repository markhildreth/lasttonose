<%inherit file="/base.mako"/>

<%def name="content()">
	<h3>Last to Nose must...<span class="game_name">${game['name']}</span></h3>
	
	<div class="nose-touch-status">
		% for name in game['participants'].keys():
		<div class="participant">
				<form action="/touch_nose" method="post" class="nose-touch">
					<input type="hidden" name="game" value="${game['id']}"/>
					<input type="hidden" name="participant" value="${name}"/>
					<input type="image" src="/static/images/nose.jpg"/>
				</form>
				<p class="name">${name}</p>
		</div>
		% endfor
	</div>
</%def>
