<template>
    <v-dialog
      v-model="value"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar
          dark
          color="#385F73"
        >
          <v-btn
            icon
            dark
            @click="$emit('closeDialog')"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-title>
          {{buttonData.default_text}}
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="4" v-if="emptyLanguageChoices.length > 0">
              <v-card>
                <v-card-title>
                  Create new translate
                </v-card-title>
                <v-card-text>
                  <v-combobox
                    v-model="newTranslateLanguageId"
                    :items="emptyLanguageChoices"
                    label="Choose language variant"
                    item-text="name"
                    item-value="id"
                    outlined
                    dense
                  ></v-combobox>
                  <v-text-field label="Translated text" v-model="newTranslateText">

                  </v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-btn @click="crateTranslate">
                    Create
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
            <v-col cols="4" v-for="translate in translates" :key="translate.id">
              <v-card>
                <v-card-title>
                  <div># {{translate.id}}: {{getLanguageById(translate.language)[0].name}}</div>
                </v-card-title>
                <v-card-text>
                  <v-text-field v-model="translate.text"></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-btn>
                    Save
                  </v-btn>
                  <v-btn>
                    Remove
                  </v-btn>
                </v-card-actions>
              </v-card>

            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
</template>

<script>
    export default {
      model: {
        prop: 'value'
      },
      props: {
        value: Boolean,
        buttonData: Object,
        languagesData: Array
      },
      data () {
        return {
          translates: [],
          newTranslateText: null,
          newTranslateLanguageId: null
        }
      },
      watch: {
        buttonData (newValue) {
          this.setTranslates(newValue.id)
        }
      },
      computed: {
        labelsList () {
          return this.translates.map(a => a.language) || []
        },
        emptyLanguageChoices () {
          return this.languagesData.filter(item => this.labelsList.indexOf(item.id) < 0)
        }
      },
      methods: {
        setTranslates (buttonId) {
          this.$axios.get(
            '/quiz/buttons/' + buttonId + '/get_translates/'
          )
            .then( response => {
              this.translates = response.data
            })
        },
        crateTranslate () {
          this.$axios.post(
            '/quiz/translates/button/',
            {
              language_id: this.newTranslateLanguageId.id,
              button_id: this.buttonData.id,
              text: this.newTranslateText
            }
          )
            .then(response => {
              this.translates.push(response.data)
            })
        },
        getLanguageById ( languageId ) {
          return this.languagesData.filter(item => item.id === languageId)
        }
      }
    }
</script>

<style scoped>

</style>
