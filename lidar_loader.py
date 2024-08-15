# test_import_lidar.py
class LIDARLoader:
    pass


from lidar_loader import LIDARLoader
try:
    from lidar_loader import LIDARLoader
    print("Importação bem-sucedida!")
except ModuleNotFoundError as e:
    print("Erro de importação:", e)
