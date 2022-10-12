from matplotlib.colors import to_rgb


palette = {
        'PosIonizable': '#3498DB',  # Blue
        'NegIonizable': '#884EA0',  # Purple
        'Acceptor': '#B03A2E',  # Red
        'Donor': '#17A589',  # Green
        'Hydrophobe': '#F5B041',  # Orange
        'LumpedHydrophobe': '#BA4A00',  # Orange
        'Aromatic': '#F1C40F',  # Yellow
    }


def add_sphere_to_view(view, center, radius, color, name):
    """ Add a sphere to a view. """
    n_components = len(view._ngl_component_ids)
    view.shape.add_sphere(center.tolist(), to_rgb(color), radius, name)
    view.update_representation(component=n_components, repr_index=0, opacity=0.5)

    
def add_features_to_view(view, feats_center, convert=True):
    """ Add chemical features to a view.
        
        Parameters
        ----------
        view: nv.NGLWidget
        feats_center : dict[str, list[np.ndarray]]
    """
    for feat_name, centroid_list in feats_center.items():
        for ii, centroid in enumerate(centroid_list):
            name = feat_name + " " + str(ii)
            if convert:
                # convert to angstroms
                centroid *= 10
            add_sphere_to_view(view, centroid, 
                               1.0, palette[feat_name], name)
