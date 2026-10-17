def freeze_loft_result(part_doc, part,part_body, target_hss, loft_obj,
                       loft_name=None,
                       delete_original=False):
    """
    将 Loft 特征通过 PasteSpecial -> AsResult 冻结为死几何 (无链接)。

    :param part_doc: CATIA PartDocument
    :param part: CATIA Part
    :param part_body: CATIA PartBody (工作对象)
    :param target_hss:
    :param loft_obj: 要冻结的 Loft (HybridShapeLoft)
    :param loft_name: 要冻结的 Loft的名字
    :param delete_original: 是否删除原 Loft
    :return: 冻结后的新 Loft 对象
    """
    selection = part_doc.selection
    selection.clear()
    selection.add(loft_obj)
    selection.copy()
    # 设置工作对象
    part.in_work_object = part_body

    # 粘贴为结果（无链接）
    try:
        selection.paste_special("CATPrtResultWithOutLink")
    except Exception as e:
        raise RuntimeError(f"PasteSpecial 失败: {e}")
    # 粘贴后两个loft名字一样
    active_loft = target_hss.item(target_hss.count)
    active_loft.name = f"{loft_name}_active"

    # 删除原始 Loft
    if delete_original:
        selection.clear()
        selection.add(active_loft)
        selection.delete()

    return new_loft

