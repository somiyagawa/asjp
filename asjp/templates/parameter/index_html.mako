<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameters')}</%block>

<h2>${title()}</h2>
<ul class="unstyled inline">
% for p in request.db.query(h.models.Parameter).order_by(h.models.Parameter.pk):
    <li>${h.link(request, p)}</li>
% endfor
</ul>
