# Copyright (c) 2010-2013 by Yaco Sistemas <goinnn@gmail.com> or <pmartin@yaco.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this programe.  If not, see <http://www.gnu.org/licenses/>.

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from testing.multimediaresources.models import Resource


def multimediaresources_index(request):
    return render_to_response('multimediaresources/index.html',
                              {'resources': Resource.objects.all()},
                              context_instance=RequestContext(request))


def multimediaresources_edit(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    return render_to_response('multimediaresources/edit.html',
                              {'resource': resource},
                              context_instance=RequestContext(request))
