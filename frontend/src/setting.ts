let backend_address = 'http://localhost:8002'

const URL = {
  get_text_list: `${backend_address}/get_text_list`,
  create_text: `${backend_address}/create_text`,
  update_text: `${backend_address}/update_text`,
  delete_text: `${backend_address}/delete_text`,
  import_data_json: `${backend_address}/import_data_json`,
  import_data: `${backend_address}/import_data`,
  export: `${backend_address}/export`, // 后面加 ann/text 等
  get_label_list: `${backend_address}/get_label_list`,
  create_label: `${backend_address}/create_label`,
  update_label: `${backend_address}/update_label`,
  delete_label: `${backend_address}/delete_label`,
  update_ann: `${backend_address}/update_ann`,
  upload_ann: `${backend_address}/upload_ann`,
}
export default URL
