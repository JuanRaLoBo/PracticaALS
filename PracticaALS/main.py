#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2
from google.appengine.ext import ndb

class Pelicula(ndb.Model):
	nombre = ndb.StringProperty(required = True)
	fecha = ndb.StringProperty(required = True)
	genero = ndb.StringProperty(required = True)

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=["jinja2.ext.autoescape"],
	autoescape=True)


class MovieHandler(webapp2.RequestHandler):

	  def load_input(self):
				self.nombre = self.request.get("nombre")
				self.fecha = self.request.get("fecha")
				self.genero = self.request.get("genero")
	  
	  def post(self):
				self.load_input()
				self.nombre = self.nombre[0].upper() + self.nombre[1:]
				self.genero = self.genero[0].upper() + self.genero[1:]
				
				# Store the answer
				movie = Pelicula(nombre = self.nombre, fecha = self.fecha, genero = self.genero);
				movie.put();
				
				self.redirect("/")
	
	
	  def get(self):
				template_values = {
					'add': 1
				}
				
				template = JINJA_ENVIRONMENT.get_template("answer.html")
				self.response.write(template.render(template_values));

				
class ListHandler(webapp2.RequestHandler):

	  def load_input(self):
				self.nombre = self.request.get("movie_to_delete")
				
	  def post(self):
				
				self.load_input()

				# Recupera la lista con todos los datos
				movies = Pelicula.query();
				
				for movie in movies:
					if movie.nombre == self.nombre:
						movie.key.delete()
				
				# Prepara la plantilla con la respuesta
				template_values = {
					'movies': movies,
					'list': 1
				}
				
				template = JINJA_ENVIRONMENT.get_template("answer.html")
				self.response.write(template.render(template_values));
	
	  def get(self):
				
				# Recupera la lista con todos los datos
				movies = Pelicula.query();
				
				# Prepara la plantilla con la respuesta
				template_values = {
					'movies': movies,
					'list': 1
				}
				
				template = JINJA_ENVIRONMENT.get_template("answer.html")
				self.response.write(template.render(template_values));
				


app = webapp2.WSGIApplication([
	('/add', MovieHandler),
	('/list', ListHandler),
], debug=True)

