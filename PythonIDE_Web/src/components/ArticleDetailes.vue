<template>
  <h1>修改文章   id={{id}}</h1>
  <h2>报错：</h2>
  <el-input v-model="article_form.error"/>
  <h2>原因：</h2>
  <el-input v-model="article_form.reason"/>
  <h2>解决方案：</h2>
  <el-input v-model="article_form.body"/>

  <el-row>
    <el-button @click="enter">确定</el-button>
    <el-button @click="delete_article">删除文章</el-button>
  </el-row>
</template>

<script setup>
import {reactive, ref, watch} from "vue";
import {onUpdated} from "vue";
import {onMounted} from "vue";
import axios from "axios";

function delete_article(){
  axios.post("http://127.0.0.1:1024/article/delete",{"id":props.id}).then(function (res){
    alert(res.data.message)
    location.reload()
  }).catch(function (err){
    console.log(err)
  })
}



function enter(){
  axios.post("http://127.0.0.1:1024/article/change",{"id":props.id,"error":article_form.error,"reason":article_form.reason,"body":article_form.body}).then(function (res){
    alert(res.data.message)
    location.reload()
  }).catch(function (err){
    console.log(err)
  })
}



onMounted(()=>{
  id.value=props.id
  axios.post("http://127.0.0.1:1024/article/article_details",{'id':props.id}).then(function (res){
    article_form.error = res.data.articledetails[0][0]
    article_form.reason = res.data.articledetails[0][1]
    article_form.body = res.data.articledetails[0][2]
  }).catch(function (err){
    console.log(err)
  })
})

const id=ref()

watch(id,(newId)=>{
  axios.post("http://127.0.0.1:1024/article/article_details",{'id':props.id}).then(function (res){
    article_form.error = res.data.userdetails[0][0]
    article_form.reason = res.data.userdetails[0][1]
    article_form.body = res.data.userdetails[0][2]
  }).catch(function (err){
    console.log(err)
  })
})



onUpdated(()=>{
  id.value=props.id
})

let article_form=reactive({
  error:"",
  reason:"",
  body:""
})

const props = defineProps({
  id:{type:String},
})
</script>