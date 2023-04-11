const { defineConfig } = require('@vue/cli-service')
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')


module.exports = defineConfig({
  transpileDependencies: true,
  devServer:{
    port:8080,
    host:'127.0.0.1',
    open:true,
    proxy:{
      '/api':{
        target:'http://localhost:9000/api/',
        ws:true,
        changeOrigin:true,
        pathRewrite:{
          '^/api':''
        }
      },
      '/wapi':{
        target:'ws://localhost:9000/api/',
        ws:true,
        changeOrigin:true,
        pathRewrite:{
          '^/wapi':''
        }
      },
    }
  },
  lintOnSave:false,
  configureWebpack: {
    plugins: [
      AutoImport({
        resolvers: [ElementPlusResolver()],
      }),
      Components({
        resolvers: [ElementPlusResolver()],
      }),
    ],
  },
})
