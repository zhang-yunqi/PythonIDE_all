<template>
<el-menu v-for="item in items" @select="(index)=> $emit('cl',index)">
  <el-menu-item :index="item[0]" >{{item[1]}}</el-menu-item>
</el-menu>
</template>

<script setup>
import {ref} from "vue";
import {onMounted} from "vue";

let items=ref()
import axios from 'axios'
onMounted(()=>{
  if (props.type==="article"){
    axios.post("http://127.0.0.1:1024/article/get_error").then(function (res){
      if(res.data.error_name.length===0){
        alert("仓库中没有文章")
      }else{
        items.value=res.data.error_name
      }
    }).catch(function (err){
      console.log(err)
    })
  }
  else if(props.type==="user"){
    axios.post("http://127.0.0.1:1024/user/getname").then(function (res){
      if(res.data.usernames.length === 0){
        alert("仓库中没有用户")
      }else{
        items.value = res.data.usernames
      }
    }).catch(function (err){
      console.log(err)
    })
  }
})


let props=defineProps({
  type:{
    type:String,
  },
})

</script>