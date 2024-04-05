import numpy as np
import streamlit as st
from streamlit_pills import pills
import plotly.graph_objects as go

from numpy_plot import dict_color_scale, parse, ParseError

class App:
	def __init__(self):
		self.set_title()
		self.set_sidebar_weight()
		self.get_coords_range()
		self.get_color_scale()
		self.get_fig_config()
		self.get_z_expression()
		self.compute_z()
		self.compute_fig()
		self.plot_fig()

	def set_title(self):
		st.set_page_config(
			page_title='Surface Plot', 
			page_icon='🏔️', 
			layout='centered', 
			initial_sidebar_state='auto'
		)

		st.title('Numpy Surface Plot')

		st.info('App in development. Many formulas will cause errors.', icon='🤖')

	def set_sidebar_weight(self):
		st.markdown(
			'''
			<style>
				section[data-testid='stSidebar'] {
					width: 600px !important; # Set the width to your desired value
				}
			</style>
			''',
			unsafe_allow_html=True,
		)

	def get_coords_range(self):
		self.x_min, self.x_max = st.sidebar.slider(
			label='X Range',
			min_value=-20.0, max_value=20.0,
			value=[-10.0, 10.0],
			step=0.1,
			key='x range'
		)
		self.y_min, self.y_max = st.sidebar.slider(
			label='Y Range',
			min_value=-20.0, max_value=20.0,
			value=[-10.0, 10.0],
			step=0.1,
			key='y range'
		)
	
	def get_color_scale(self):
		col_pills, col_selectbox = st.sidebar.columns((1,4))
		with col_pills:
			color_scale_type = pills(
				label='Color type',
				options=[
					'Categorical', 
					'Sequential', 
					'Diverging',
				]
			)
		self.color_scale = col_selectbox.selectbox(
			label='Color scale',
			key='color scale',
			options=dict_color_scale[color_scale_type],
			index=0
		)
	
	def get_fig_config(self):
		col_projection, col_show_colorscale, _ = st.sidebar.columns(3)
		self.show_projection = col_projection.toggle(
			label='Projection',
			value=True,
			key='projection'
		)
		self.show_colorscale = col_show_colorscale.toggle(
			label='Show scale',
			value=False,
			key='show scale'
		)

	def get_z_expression(self):
		self.z_expression = st.sidebar.text_area(
			label='Z expression',
			value='(x + y) / (2 + cos(x) * sin(y))',
			key='z expression'
		)

	def compute_z(self):
		
		self.x_axis = np.linspace(self.x_min, self.x_max, num=1000)
		self.y_axis = np.linspace(self.y_min, self.y_max, num=1000)
		
		x = self.x_axis.reshape((-1, 1))
		y = self.y_axis.reshape((1, -1))

		self.z = parse(self.z_expression, x, y)
		if isinstance(self.z, ParseError):
			st.sidebar.error(icon='🚫', body=self.z.message)
		elif self.z.shape != (1000, 1000):
			st.sidebar.error('Invalid expression.')

	def compute_fig(self):
		self.fig = go.Figure(go.Surface(
			x=self.x_axis, y=self.y_axis, z=self.z,
			colorscale=self.color_scale,
			showscale=self.show_colorscale
		))

		self.fig.update_layout(
			height=900,
			margin=dict(l=0, r=0, b=0, t=0), 
			scene={'camera': {'eye': {
				'x' : -2.0, 
				'y' : -2.0,
				'z' : 0.75,
			}}},
		)

		if self.show_projection:
			self.fig.update_traces(
				contours_z=dict(
					show=True, 
					usecolormap=True,
					highlightcolor='#f2e9e4', 
					project_z=True
				)
			)

	def plot_fig(self):
		st.plotly_chart(self.fig, use_container_width=True)
