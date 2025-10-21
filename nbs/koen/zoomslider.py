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

        self.display_height_setting = pn.widgets.IntInput(
            value=650, 
            name='Display height:',
            placeholder='Please enter your display height.'
        )
        
        self.settings = pn.WidgetBox(
            pn.pane.Markdown("## Settings"),
            self.display_height_setting
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
            'display_height' : self.display_height_setting.value,
        }
        left_im, width = self._convert_image(self.file_upload.value[0], **settings)
        right_im, _ = self._convert_image(self.file_upload.value[1], **settings)
        
        self.slider = pn.layout.Swipe(left_im, right_im, slider_color='red', width=width)
        self.main.clear()
        self.main.extend([
                self.title,
                self.slider
            ])
        
    def _convert_image(self, im, display_height=650):
        io_im = iio.imread(im)
        aspect_ratio = io_im.shape[1] / io_im.shape[0]
        width = int(display_height * aspect_ratio)
        if len(io_im.shape) == 2:
            hv_im = hv.Image(io_im)
            rast_im = rasterize(hv_im)
            return pn.pane.HoloViews(rast_im.opts(xaxis=None, yaxis=None, toolbar=None, cmap="gray", height=display_height, width=width)), width
        elif len(io_im.shape) == 3:
            hv_im = hv.RGB(io_im)
            rast_im = rasterize(hv_im)
            return pn.pane.HoloViews(rast_im.opts(xaxis=None, yaxis=None, toolbar=None, height=display_height, width=width)), width
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