# coding: utf-8
import ui,console
from functools import partial,wraps

def animated(duration):
	'''Animate calls to the decorated method, using specified duration.
todo: add completion which gets called on the self object after animation is done.'''
	def decorator(fcn):
		@wraps(fcn)
		def animation(self):
			ui.animate(partial(fcn,self),duration=duration)
		return animation
	return decorator

GESTURELENGTH=40	#distance of touch drag before any menus are shown

class SplitView(ui.View):
	'''A simple split view implemented without objc.
	set .mainview to your view. will be added, and resized to fit
	set .detailview, will be added and resized to fit.
	detailwidth sets widh of detail pane, defaults to 320
	style: 'slide' slides mainview over
	        'overlap' slides detail overlapping main.
	delegate, a custom delegate which implements splitview_did_show(splitview) and/or splitview_did_hide(splitview)
	
	sliding right in main view shows the detail.
	sliding left hides the detail pane
	'''
	def __init__(self,detailwidth=320,style='slide',delegate=None,**kwargs):
		ui.View.__init__(self,**kwargs)
		self._sv=ui.ScrollView()
		self._sv.flex='wh'
		self._sv.frame=self.bounds
		self._sv.content_size=(self.bounds[2]+1,self.bounds[3])
		self._mainviewcontainer=ui.View()
		self._mainviewcontainer.frame=self.bounds
		self._detailviewcontainer=ui.View()
		self._detailviewcontainer.frame=self.bounds
		self.detailwidth = detailwidth
		self._detailviewcontainer.width=detailwidth
		self._detailviewcontainer.x=-detailwidth
		self._mainviewcontainer.flex='WH'
		self._detailviewcontainer.flex='H'
		self._mainview=None
		self._detailview=None
		self.delegate=delegate
		self._sv.delegate=self
		self._sv.add_subview(self._mainviewcontainer)
		self._sv.add_subview(self._detailviewcontainer)
		self.add_subview(self._sv)
		self.style='slide'# 'slide','resize'
		self.state=0 #1 when detail shown

	def scrollview_did_scroll(self, scrollview):
		if not scrollview.dragging:
			if self.state==0 and scrollview.content_offset[0]<-GESTURELENGTH:
				self.show_detail()
			if self.state==1 and scrollview.content_offset[0]>GESTURELENGTH:
				self.hide_detail()
	@animated(0.3)
	def show_detail(self):
		'''shows the detail view, and calls splitview_did_show(self) on the delegate'''
		self._detailviewcontainer.x=0
		if self.style=='slide':
			self._mainviewcontainer.x=self.detailwidth
		if self.state==0 and hasattr(self.delegate,'splitview_did_show'):
			self.delegate.splitview_did_show(self)
		self.state=1
	
	@animated(0.2)
	def hide_detail(self):
		'''hides the detail view, and calls splitview_did_hide(self) on the delegate'''
		self._detailviewcontainer.x = -self._detailviewcontainer.width
		self._mainviewcontainer.x=0
		if self.state==1 and hasattr(self.delegate,'splitview_did_hide'):
			self.delegate.splitview_did_hide(self)
		self.state=0
	def toggle_detail(self):
		if self.state==1:
			self.hide_detail()
		else:
			self.show_detail()

	@property
	def mainview(self):
		return self._mainview
	@mainview.setter
	def mainview(self,value):
		if self._mainview:
			self._mainviewcontainer.remove_subview(self._mainview)
		self._mainview=value
		self._mainviewcontainer.add_subview(self._mainview)
		self._mainview.frame=self._mainviewcontainer.bounds
	@property
	def detailview(self):
		return self._detailview
	@detailview.setter
	def detailview(self,value):
		if self._detailview:
			self._detailviewcontainer.remove_subview(self._detailview)
		self._detailview=value
		self._detailviewcontainer.add_subview(self._detailview)
		self._detailview.frame=self._detailviewcontainer.bounds

	
if __name__=='__main__':
	splitview=SplitView(frame=(0,0,768,768),bg_color=(1,1,1))

	#create a mainview. could be loaded from pyui, etc
	mainview=ui.View(frame=(0,0,768,768))
	tv=ui.TextView(frame=(100,100,300,500),bg_color=(.9,1,1),flex='wh')
	mainview.add_subview(tv)
	mainview.add_subview(ui.Button(name='menu',frame=(30,0,44,44),image=ui.Image.named('iob:drag_32')))
	def toggle(sender):
		splitview.toggle_detail()
	mainview['menu'].action=toggle
	tv.text='Select font from side menu, by pushing button or dragging (not on a component)'

	# create a detail view.  
	detailview=ui.View()
	tbl=ui.TableView()
	tbl.data_source=ui.ListDataSource(['Courier','Menlo','Menlo-Bold','Zapfino','AmericanTypewriter'])
	tbl.delegate=tbl.data_source
	def font_selected(sender):
		tv.font=(sender.items[sender.selected_row],tv.font[1])
	tbl.data_source.action=font_selected
	tbl.flex='wh'
	detailview.add_subview(tbl)
	
	#add to splitview
	splitview.mainview=mainview
	splitview.detailview=detailview

	#example delegate, tracks button color to detail state
	class ButtonToggler(object):
		def __init__(self,btn):
			self.target=btn
		def splitview_did_hide(self,splitview):
			self.target.bg_color=(0,0,0,0)
		def splitview_did_show(self,splitview):
			self.target.bg_color=(.9,.8,.8,1)
	splitview.delegate=ButtonToggler(mainview['menu'])
	splitview.present('panel')
	

	