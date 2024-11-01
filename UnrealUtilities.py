from unreal import (
    AssetToolsHelpers,
    AssetTools,
    EditorAssetLibrary,
    Material,
    MaterialFactoryNew,
    MaterialProperty,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TextSample2D,
    AssetImportTask,
    FbxImportUI
)

import os

class UnrealUtility:
    def __init__(self):
        # Initialize paths and names for the substance material and its components
        self.substanceRootDir = "/Game/Substance/"
        self.baseMaterialName = "M_SubstanceBase"
        self.substanceTempDir = "/Game/Substance/Temp/"
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetalicName = "OcclusionRoughnessMetallic"

    def FindOrCreateBaseMaterial(self):
        # Check if the base material already exists
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)

        # Create a new base material if it doesn't exist
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(
            self.baseMaterialName, self.substanceRootDir, Material, MaterialFactoryNew()
        )

        # Create a texture sample for BaseColor and connect it to the material
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        # Create a texture sample for Normal and connect it to the material
        normal = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)

        # Create a texture sample for Occlusion, Roughness, and Metallic and connect it to the material
        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 800)
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalicName)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)

        # Save the newly created material
        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat

    def LoadMeshFromPath(self, meshPath):
        # Extract the mesh name from the provided path
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")
        importTask = AssetImportTask()
        importTask.replace_existing = True  # Replace existing assets if they exist
        importTask.filename = meshPath  # Set the path for the mesh to import
        importTask.destination_path = "/Game/" + meshName  # Set the destination path in the Unreal project
        importTask.save = True  # Save the asset after import
        importTask.automated = True  # Run the import automatically

        # Set up FBX import options
        fbxImportOptions = FbxImportUI()
        fbxImportOptions.import_mesh = True  # Import mesh data
        fbxImportOptions.import_as_skeletal = False  # Import as static mesh
        fbxImportOptions.import_materials = False  # Do not import materials from FBX
        fbxImportOptions.static_mesh_import_data.combine_meshes = True  # Combine meshes during import

        # Assign the import options to the task
        importTask.options = fbxImportOptions

        # Execute the import task
        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]  # Return the imported mesh object

    def LoadFromDir(self, fileDir):
        # Iterate through all files in the specified directory
        for file in os.listdir(fileDir):
            # Check if the file is an FBX file
            if file.endswith(".fbx"):
                # Load the mesh from the file path
                self.LoadMeshFromPath(os.path.join(fileDir, file))