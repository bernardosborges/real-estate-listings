# import pytest
# from unittest.mock import MagicMock, patch, AsyncMock

# from app.services.property_tag_service import PropertyTagService
# from app.core.exceptions.domain_exception import PropertyNotFound, TagNotFound


# @pytest.fixture
# def mock_property():
#     from app.models.property_model import PropertyModel
#     return PropertyModel(id=1, description="Apartamento teste")

# @pytest.fixture
# def mock_tag():
#     from app.models.tag_model import TagModel
#     tag = TagModel(id=10, slug="tag-teste", name="Tag Teste", group_id=None)
#     tag.group = None
#     return tag

# class TestValidatePropertyExists:

#     def test_validate_property_exists_returns_property(self, mock_property):
#         property_id = 1
#         mock_db = MagicMock()
#         with patch("app.services.property_tag_service.PropertyRepository.get_property", return_value=mock_property) as mock_get_property:
#             result = PropertyTagService.validate_property_exists(db=mock_db, property_id=property_id)
#             assert result == mock_property
#             mock_get_property.assert_called_once_with(mock_db, property_id)


#     def test_validate_property_exists_not_found(self, mock_property):
#         property_id = 999
#         mock_db = MagicMock()
#         with patch("app.services.property_tag_service.PropertyRepository.get_property", return_value=None) as mock_get_property:
#             with pytest.raises(PropertyNotFound):
#                 PropertyTagService.validate_property_exists(mock_db, property_id=property_id)
#             mock_get_property.assert_called_once_with(mock_db, property_id)

# class TestAddTagsToProperty:

#     def test_add_tags_to_property_success(self, mock_property, mock_tag):
#         property_id = mock_property.id
#         tags_slug = ["tag-teste"]
#         mock_db = MagicMock()
#         mock_tag.group = None

#         with patch("app.services.property_tag_service.PropertyTagService.validate_property_exists", return_value=mock_property) as mock_validate, \
#              patch("app.services.property_tag_service.TagRepository.get_by_slug", return_value=mock_tag) as mock_get_tag, \
#              patch("app.services.property_tag_service.PropertyTagRepository.hard_delete_exclusive_group") as mock_hard_delete, \
#              patch("app.services.property_tag_service.PropertyTagRepository.get_by_property_and_tag", return_value=None) as mock_get_property_tag, \
#              patch("app.services.property_tag_service.PropertyTagRepository.create", return_value=[MagicMock(tag_id=mock_tag.id)]) as mock_create, \
#              patch("app.services.property_tag_service.PropertyTagService.list_tags_for_property", return_value={"property_id": property_id, "tags": [{"tag_slug": mock_tag.slug, "tag_name": mock_tag.name}]}) as mock_list_tags:

#             result = PropertyTagService.add_tags_to_property(db=mock_db, property_id=property_id, tags_slug=tags_slug)

#             assert result == {"property_id": property_id, "tags": [{"tag_slug": "tag-teste", "tag_name": "Tag Teste"}]}

#             mock_validate.assert_called_once_with(mock_db, property_id)
#             mock_get_tag.assert_called_once_with(mock_db, "tag-teste")
#             mock_get_property_tag.assert_called_once_with(mock_db, property_id, mock_tag.id)
#             mock_create.assert_called_once()
#             mock_list_tags.assert_called_once_with(mock_db, property_id)
