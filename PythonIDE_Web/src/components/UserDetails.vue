<template>
  <h1>修改用户   id={{id}}</h1>
  <h2>用户名：</h2>
  <el-input v-model="user_form.user_name"/>
  <h2>密码：</h2>
  <el-input v-model="user_form.password"/>
  <h2>等级：</h2>
  <el-input v-model="user_form.user_level"/>
  <el-row>
    <el-button @click="enter">确定</el-button>
    <el-button @click="delete_user">删除用户</el-button>
  </el-row>
</template>

<script setup>
import {reactive, ref, watch} from "vue";
import {onMounted} from "vue";
import {onUpdated} from "vue";
import axios from "axios";

function delete_user(){
  axios.post("http://127.0.0.1:1024/user/delete",{"id":props.id}).then(function (res){
    alert(res.data.message)
    location.reload()
  }).catch(function (err){
    console.log(err)
  })
}



function enter(){
  axios.post("http://127.0.0.1:1024/user/change",{"id":props.id,"name":user_form.user_name,"password":user_form.password,"level":user_form.user_level}).then(function (res){
    alert(res.data.message)
    location.reload()
  }).catch(function (err){
    console.log(err)
  })
}


onMounted(()=>{
  id.value=props.id
  axios.post("http://127.0.0.1:1024/user/user_details",{'id':props.id}).then(function (res){
    user_form.user_name = res.data.userdetails[0][0]
    user_form.password = res.data.userdetails[0][1]
    user_form.user_level = res.data.userdetails[0][2]
  }).catch(function (err){
    console.log(err)
  })
})
const id=ref()

watch(id,(newId)=>{
  axios.post("http://127.0.0.1:1024/user/user_details",{'id':props.id}).then(function (res){
    user_form.user_name = res.data.userdetails[0][0]
    user_form.password = res.data.userdetails[0][1]
    user_form.user_level = res.data.userdetails[0][2]
  }).catch(function (err){
    console.log(err)
  })
})



onUpdated(()=>{
  id.value=props.id
})

let user_form=reactive({
  user_name:"",
  user_level:0,
  password:""
})

const props = defineProps({
  id:{type:String},
})
</script>