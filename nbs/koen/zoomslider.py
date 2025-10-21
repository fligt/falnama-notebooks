import imageio.v3 as iio
import holoviews as hv
from holoviews.operation.datashader import rasterize 
import panel as pn

hv.extension('bokeh')
pn.extension(sizing_mode='stretch_width')

class ZoomSlider():

    def __init__(self):
        self._build_ui()

    def _build_ui(self):
        self.title = pn.pane.Markdown("# ZoomSlider")
        
        self.file_upload = pn.widgets.FileSelector('./Images/', only_files=True)
        
        self.upload_button = pn.widgets.Button(
            name="Load images",
            button_type="primary"
        )
        self.upload_button.on_click(self._create_slider)

        self.rast_size_setting = pn.widgets.IntInput(
            value=1000, 
            name='Raster size:',
            placeholder='Please enter your raster size.'
        )

        self.display_width_setting = pn.widgets.IntInput(
            value=600,
            name='Display width:',
            placeholder='Please enter your display width.'
        )

        self.display_height_setting = pn.widgets.IntInput(
            value=600, 
            name='Display height:',
            placeholder='Please enter your display height.'
        )
        
        self.settings = pn.WidgetBox(
            pn.pane.Markdown("## Settings"),
            self.rast_size_setting,
            #self.display_width_setting,
            #self.display_height_setting
        )

        self.reset_button = pn.widgets.Button(
            name="Reset",
            button_type="danger"
        )
        
        self.reset_button.on_click(self._reset_view)
        
        self.sidebar = pn.Column(
            pn.pane.Markdown("## File Selection"),
            pn.pane.Markdown("### Upload 2 files to start."),
            self.settings,
            self.reset_button
        )
    
        self.main = pn.Column(
            self.title,
            self.file_upload,
            self.upload_button
        )
    
        self.template = pn.template.FastListTemplate(
            title="ZoomSlider",
            sidebar=[self.sidebar],
            main=[self.main]
        )

    def _create_slider(self, event):
        self.main.clear()
        self.main.append(pn.pane.Markdown("Converting images..."))

        settings = {
            'rast_size' : self.rast_size_setting.value,
            #'display_width' : self.display_width_setting.value,
            #'display_height' : self.display_height_setting.value
        }
        left_im = self._convert_image(self.file_upload.value[0], **settings)
        right_im = self._convert_image(self.file_upload.value[1], **settings)
        
        self.slider = pn.layout.Swipe(left_im, right_im, slider_color='red', width=600)
        self.main.clear()
        self.main.extend([
                self.title,
                self.slider
            ])
        
    def _convert_image(self, im, rast_size=1000):
        io_im = iio.imread(im)
        if len(io_im.shape) == 2:
            hv_im = hv.Image(io_im)
            rast_im = rasterize(hv_im, width=rast_size, height=rast_size)
            return pn.pane.HoloViews(rast_im.opts(xaxis=None, yaxis=None, toolbar=None, cmap="gray"))
        elif len(io_im.shape) == 3:
            hv_im = hv.RGB(io_im)
            rast_im = rasterize(hv_im, width=rast_size, height=rast_size)
            return pn.pane.HoloViews(rast_im.opts(xaxis=None, yaxis=None, toolbar=None))
        else:
            raise ValueError(f"Image shape not recognized, needs to be 2 or 3 but found {io_im.shape}")

    def _reset_view(self, event):
        print("RESETTING RESETTING RESETTING!!!")
        self.main.clear()
        self.main.extend([
            self.title,
            self.file_upload,
            self.upload_button
        ])

app = ZoomSlider()
app.template.servable()