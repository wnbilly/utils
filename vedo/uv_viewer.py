from vedo import Points, Point, Image, Mesh, Plotter, utils

DEFAULT_PT = [0, 0, 0]
VERTICES_RADIUS = 5
VERTICES_COLOR = 'blue'


# Based on the code example of https://vedo.embl.es/docs/vedo/utils.html#get_uv made in this forum post https://forum.image.sc/t/getting-uv-coordinates-of-a-textured-mesh/70816
class UVviewer:

    def __init__(self, mesh_path, texture_path, uv=None, display_vertices=False):

        # Init the mesh and its texture
        self.texture = Image(texture_path)
        self.mesh = Mesh(mesh_path).lighting("off").texture(self.texture, repeat=False)

        self.display_vertices = display_vertices

        # self.mesh.compute_normals()
        if uv is not None:
            self.uv = uv
        else:
            # It appears that .stl, .ply, .vtk files use "Texture Coordinates" and some .obj files use "Material"
            self.uv = self.mesh.pointdata["Material"] if self.mesh.pointdata["Material"] is not None else self.mesh.pointdata["Texture Coordinates"]

        self.selected_point_in_plotter = DEFAULT_PT
        self.selected_point_on_mesh = self.mesh.closest_point(self.selected_point_in_plotter)
        self.i_interp_uv = None
        self.compute_ix_iy()

        # Plotter utils
        self.plotter = None

    def compute_ix_iy(self):
        self.selected_point_on_mesh = self.mesh.closest_point(self.selected_point_in_plotter)

        selected_face_id = self.mesh.closest_point(self.selected_point_in_plotter, return_cell_id=True)
        selected_face = self.mesh.cells[selected_face_id]
        uv_of_selected_face = self.uv[selected_face]

        # See https://vedo.embl.es/docs/vedo/utils.html#get_uv
        uv_of_selected_point_on_mesh = utils.get_uv(self.selected_point_on_mesh, self.mesh.vertices[selected_face], uv_of_selected_face)

        self.i_interp_uv = uv_of_selected_point_on_mesh * self.texture.dimensions()

        closest_vertice_id = self.mesh.closest_point(self.selected_point_in_plotter, return_point_id=True)
        print(f"\nSelected point on mesh : {self.selected_point_on_mesh}"
              f"\nuv of selected point : {uv_of_selected_point_on_mesh}"
              f"\nClosest vertice id = {closest_vertice_id}"
              f"\nClosest vertice coordinates = {self.mesh.vertices[closest_vertice_id]}")

    # callback function
    def __on_left_click__(self, event):
        if not event.object:
            return
        else:
            if event.at == 0:
                self.selected_point_in_plotter = event.picked3d
                self.compute_ix_iy()
                self.update_plotter_objects()

    def init_plotter(self):
        # Initialize a Plotter instance
        self.plotter = Plotter(N=2, axes=1, sharecam=False, interactive=False)
        self.plotter.add_callback('LeftButtonPress', self.__on_left_click__)

        self.update_plotter_objects()

    def update_plotter_objects(self):
        # Add elements to the plotter
        left_plotter_visuals = [self.mesh, Point(self.selected_point_on_mesh)]
        if self.display_vertices:
            left_plotter_visuals += [Points(self.mesh.vertices, r=VERTICES_RADIUS, c=VERTICES_COLOR)]
        self.plotter.show(left_plotter_visuals, at=0)
        self.plotter.show(self.texture, Point(self.i_interp_uv), at=1)

    def show_plotter(self):
        if not self.plotter:
            self.init_plotter()
        # Render the plotter
        self.plotter.interactive().close()


if __name__ == "__main__":
    from vedo import dataurl

    mesh_path = dataurl + 'panther.stl'
    tex_path = dataurl + 'textures/earth0.jpg'

    viewer = UVviewer(mesh_path, tex_path)
    viewer.init_plotter()
    viewer.show_plotter()
