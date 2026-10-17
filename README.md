# CATIA yarn geometry generation

使用 Python、pycatia 和 CATScript，根据纱线路径及截面 CSV 数据在 CATIA V5 中生成纱线几何。

## 文件说明

- `creat_3DWC_geo_by_CATIA.py`：几何生成入口，包含当前使用的固定参数。
- `BuildYarnLoft.CATScript`：由 Python 脚本调用的建模宏。
- `geo_point_files13-24-24_0.rar`：路径和截面 CSV 数据压缩包，运行前需要解压。
- `user_scripts/`：随项目提供的工具脚本，包含来自 pycatia 的第三方代码。

## 运行

需要 Windows、已启动的 CATIA V5，以及包含 NumPy 和 pycatia 的 Python 环境。
使用已验证通过的 Python/pycatia 环境运行。

先将 `geo_point_files13-24-24_0.rar` 解压到本 README 所在文件夹，确保数据目录直接位于脚本旁，避免多套一层同名目录：

```text
creat_3DWC_geo_by_CATIA.py
BuildYarnLoft.CATScript
user_scripts/
geo_point_files13-24-24_0/
    warp_path_files/
    warp_section_files/
    weft_path_files/
    weft_section_files/
```

然后将终端工作目录切换至本 README 所在文件夹，执行：

```powershell
python .\creat_3DWC_geo_by_CATIA.py
```

当前脚本从运行时工作目录读取 CSV 数据并保存 CATPart；
`user_scripts` 和 `BuildYarnLoft.CATScript` 则从 Python 脚本所在目录加载。
运行前请核对脚本内固定参数与数据文件的一致性。
生成的 CATPart 文件保存在运行时工作目录中；预生成的 CATPart 文件不随仓库提供。

## 第三方代码与许可证

`user_scripts` 包含从 [pycatia](https://github.com/evereux/pycatia) 复制或改编的代码。
其中 `ToolFunctions` 对应上游的 `wing_surface_from_naca_profile_support` 目录，
`hide_show.py` 增加了显示/隐藏控制参数。

pycatia 来源代码保留原 MIT 许可证和版权声明，见
[user_scripts/LICENSE.txt](user_scripts/LICENSE.txt)。
逐文件来源、修改说明及核实范围见
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

`ToolFunctions/paste_result.py` 由项目作者自行编写，不属于 pycatia 第三方代码。
本项目自行编写的代码、宏及自有数据采用 [MIT License](LICENSE)，允许使用、修改和再分发，须保留版权及许可声明。第三方代码保留其原有版权声明及许可证。
