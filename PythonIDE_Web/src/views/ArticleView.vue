<template>
  <el-container>
    <el-header style="height: 50px;background-color: #535bf2">
      <h1>Article</h1>
    </el-header>
    <el-container>
      <el-aside style="width: 300px">
        <ListOfContent @cl="select" :type="type"></ListOfContent>
      </el-aside>
      <el-main>
        <ArticleDetailes v-if="have_item" :id="select_id"></ArticleDetailes>
      </el-main>
    </el-container>
  </el-container>
</template>

<script  setup>
import ListOfContent from '../components/ListOfContent.vue'
import {ref} from "vue";

import {onMounted} from "vue";
import axios from "axios";
let have_item=ref(false)

onMounted(()=>{
  axios.post("http://127.0.0.1:1024/article/get_error").then(function (res){
    if(res.data.error_name.length!=0){
      have_item.value=true
    }
  })
})

import ArticleDetailes from "../components/ArticleDetailes.vue";
let select_id = ref("0")
const type=ref("article")
function select(i){
  select_id.value=i
}
</script>